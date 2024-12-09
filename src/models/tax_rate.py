from sqlalchemy import Column, Integer, Float, String
from src.database.database import Base

class TaxRate(Base):
    __tablename__ = "tax_rates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # z.B. "Standard", "Reduziert"
    rate = Column(Float)   # z.B. 0.19 für 19%
    is_default = Column(Integer, default=0)  # 1 für Standard-MwSt
