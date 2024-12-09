from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.database import Base

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    
    # Relationships
    products = relationship("Product", back_populates="supplier")
