from typing import List, Optional
from sqlalchemy.orm import joinedload
from src.models.product import Product
from src.models.inventory import Inventory
from src.database.database import SessionLocal

class ProductService:
    @staticmethod
    def create_product(name: str, barcode: str, price: float, category: str = None,
                      cost_price: float = None, tax_rate: float = 0.19,
                      quantity: int = 0, minimum_stock: int = 0) -> Product:
        with SessionLocal() as db:
            product = Product(
                name=name,
                barcode=barcode,
                price=price,
                cost_price=cost_price,
                tax_rate=tax_rate,
                category=category
            )
            # Create inventory record
            inventory = Inventory(
                product=product,
                quantity=quantity,
                minimum_stock=minimum_stock
            )
            db.add(product)
            db.add(inventory)
            db.commit()
            db.refresh(product)
            return product

    @staticmethod
    def get_product(product_id: int) -> Optional[Product]:
        with SessionLocal() as db:
            return db.query(Product).options(joinedload(Product.inventory)).filter(Product.id == product_id).first()

    @staticmethod
    def get_product_by_barcode(barcode: str):
        with SessionLocal() as db:
            return db.query(Product).options(joinedload(Product.inventory)).filter(Product.barcode == barcode).first()

    @staticmethod
    def get_product_by_name(name: str):
        with SessionLocal() as db:
            return db.query(Product).options(joinedload(Product.inventory)).filter(Product.name == name).first()

    @staticmethod
    def get_all_products() -> List[Product]:
        with SessionLocal() as db:
            return db.query(Product).options(joinedload(Product.inventory)).all()

    @staticmethod
    def search_products(query: str = "") -> List[Product]:
        with SessionLocal() as db:
            products = db.query(Product).options(joinedload(Product.inventory))
            if query:
                products = products.filter(
                    Product.name.ilike(f"%{query}%") |
                    Product.barcode.ilike(f"%{query}%") |
                    Product.category.ilike(f"%{query}%")
                )
            return products.all()

    @staticmethod
    def update_product(product_id: int, **kwargs) -> Optional[Product]:
        with SessionLocal() as db:
            product = db.query(Product).options(joinedload(Product.inventory)).filter(Product.id == product_id).first()
            if product:
                # Update product attributes
                for key, value in kwargs.items():
                    if key in ['quantity', 'minimum_stock']:
                        # Handle inventory fields
                        if not product.inventory:
                            product.inventory = Inventory(product=product)
                        if key == 'quantity':
                            product.inventory.quantity = value
                        elif key == 'minimum_stock':
                            product.inventory.minimum_stock = value
                    elif hasattr(product, key):
                        setattr(product, key, value)
                
                db.commit()
                db.refresh(product)
            return product

    @staticmethod
    def delete_product(product_id: int) -> bool:
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                db.delete(product)
                db.commit()
                return True
            return False
