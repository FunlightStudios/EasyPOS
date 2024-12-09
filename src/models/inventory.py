from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.database import Base
from datetime import datetime

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    minimum_stock = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory")

    def update_stock(self, quantity_change: float):
        self.quantity += quantity_change
        self.last_updated = datetime.utcnow()

    def is_low_stock(self) -> bool:
        return self.quantity <= self.minimum_stock
