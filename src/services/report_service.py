from src.models.sale import Sale, SaleItem
from src.models.product import Product
from src.database.database import SessionLocal
from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func

class ReportService:
    @staticmethod
    def get_sales_report(start_date: datetime, end_date: datetime) -> Dict:
        with SessionLocal() as db:
            sales = db.query(Sale).filter(
                Sale.date >= start_date,
                Sale.date <= end_date,
                Sale.payment_status == "paid"
            ).all()

            total_sales = sum(sale.total_amount for sale in sales)
            avg_sale = total_sales / len(sales) if sales else 0

            return {
                "total_sales": total_sales,
                "number_of_sales": len(sales),
                "average_sale": avg_sale,
                "sales": sales
            }

    @staticmethod
    def get_product_sales_report(start_date: datetime, end_date: datetime) -> List[Dict]:
        with SessionLocal() as db:
            results = db.query(
                Product.name,
                func.sum(SaleItem.quantity).label('total_quantity'),
                func.sum(SaleItem.quantity * SaleItem.price).label('total_revenue')
            ).join(SaleItem).join(Sale).filter(
                Sale.date >= start_date,
                Sale.date <= end_date,
                Sale.payment_status == "paid"
            ).group_by(Product.id).all()

            return [{
                "product": result[0],
                "quantity_sold": result[1],
                "revenue": result[2]
            } for result in results]

    @staticmethod
    def get_inventory_report() -> List[Dict]:
        with SessionLocal() as db:
            products = db.query(Product).all()
            return [{
                "product": product.name,
                "stock": product.inventory.quantity,
                "min_stock": product.inventory.minimum_stock,
                "needs_restock": product.inventory.quantity <= product.inventory.minimum_stock
            } for product in products]

    @staticmethod
    def get_daily_summary(date: datetime = None) -> Dict:
        if not date:
            date = datetime.now()

        with SessionLocal() as db:
            sales = db.query(Sale).filter(
                Sale.date >= date.replace(hour=0, minute=0, second=0),
                Sale.date < date.replace(hour=23, minute=59, second=59),
                Sale.payment_status == "paid"
            ).all()

            payment_methods = {}
            for sale in sales:
                payment_methods[sale.payment_method] = payment_methods.get(
                    sale.payment_method, 0) + sale.total_amount

            return {
                "date": date.date(),
                "total_sales": sum(sale.total_amount for sale in sales),
                "number_of_transactions": len(sales),
                "payment_methods": payment_methods
            }
