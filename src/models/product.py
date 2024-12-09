from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    barcode = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    cost_price = Column(Float)
    tax_rate = Column(Float)
    category = Column(String)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    
    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    sale_items = relationship("SaleItem", back_populates="product")
