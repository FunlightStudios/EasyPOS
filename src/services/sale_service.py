from src.models.sale import Sale, SaleItem
from src.models.product import Product
from src.models.inventory import Inventory
from src.database.database import SessionLocal
from datetime import datetime
from typing import List, Dict, Optional

class SaleService:
    @staticmethod
    def create_sale(user_id: int, items: List[Dict], payment_method: str, customer_id: Optional[int] = None):
        with SessionLocal() as db:
            # Create sale
            sale = Sale(
                user_id=user_id,
                customer_id=customer_id,
                payment_method=payment_method,
                payment_status="paid",
                date=datetime.utcnow(),
                total_amount=0
            )
            db.add(sale)
            db.flush()  # Get sale.id without committing

            total_amount = 0
            
            # Add items and update inventory
            for item in items:
                product = db.query(Product).filter(Product.id == item['product_id']).first()
                if not product:
                    db.rollback()
                    raise ValueError(f"Product {item['product_id']} not found")

                # Check inventory
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == product.id
                ).first()
                
                if inventory.quantity < item['quantity']:
                    db.rollback()
                    raise ValueError(f"Insufficient stock for product {product.name}")

                # Create sale item
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=item['quantity'],
                    price=product.price,
                    discount=item.get('discount', 0)
                )
                db.add(sale_item)

                # Update inventory
                inventory.update_stock(-item['quantity'])
                
                # Calculate total
                item_total = (product.price * item['quantity']) * (1 - item.get('discount', 0))
                total_amount += item_total

            # Update sale total
            sale.total_amount = total_amount
            db.commit()
            return sale

    @staticmethod
    def get_sale(sale_id: int):
        with SessionLocal() as db:
            return db.query(Sale).filter(Sale.id == sale_id).first()

    @staticmethod
    def get_daily_sales(date: datetime):
        with SessionLocal() as db:
            return db.query(Sale).filter(
                Sale.date >= date.replace(hour=0, minute=0, second=0),
                Sale.date < date.replace(hour=23, minute=59, second=59)
            ).all()

    @staticmethod
    def void_sale(sale_id: int):
        with SessionLocal() as db:
            sale = db.query(Sale).filter(Sale.id == sale_id).first()
            if not sale:
                return False

            # Restore inventory
            for item in sale.items:
                inventory = db.query(Inventory).filter(
                    Inventory.product_id == item.product_id
                ).first()
                if inventory:
                    inventory.update_stock(item.quantity)

            sale.payment_status = "voided"
            db.commit()
            return True
