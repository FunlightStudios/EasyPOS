from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from src.database.database import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)
    total_amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)  # paid, pending, cancelled
    
    # Relationships
    customer = relationship("Customer", back_populates="sales")
    user = relationship("User")
    items = relationship("SaleItem", back_populates="sale")

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    price = Column(Float)
    discount = Column(Float, default=0)
    
    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")
