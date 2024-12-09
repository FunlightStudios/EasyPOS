from typing import List
from sqlalchemy.orm import Session
from src.models.tax_rate import TaxRate
from src.database.database import SessionLocal

class TaxRateService:
    @staticmethod
    def create_tax_rate(name: str, rate: float, is_default: bool = False) -> TaxRate:
        with SessionLocal() as db:
            # Wenn dieser Satz als Standard gesetzt werden soll, alle anderen zurücksetzen
            if is_default:
                TaxRateService.clear_default_tax_rate(db)
                
            tax_rate = TaxRate(
                name=name,
                rate=rate,
                is_default=1 if is_default else 0
            )
            db.add(tax_rate)
            db.commit()
            db.refresh(tax_rate)
            return tax_rate
            
    @staticmethod
    def clear_default_tax_rate(db: Session):
        db.query(TaxRate).filter(TaxRate.is_default == 1).update({"is_default": 0})
        db.commit()
            
    @staticmethod
    def get_all_tax_rates() -> List[TaxRate]:
        with SessionLocal() as db:
            return db.query(TaxRate).all()
            
    @staticmethod
    def get_default_tax_rate() -> TaxRate:
        with SessionLocal() as db:
            return db.query(TaxRate).filter(TaxRate.is_default == 1).first()
            
    @staticmethod
    def delete_tax_rate(tax_rate_id: int):
        with SessionLocal() as db:
            tax_rate = db.query(TaxRate).filter(TaxRate.id == tax_rate_id).first()
            if tax_rate:
                db.delete(tax_rate)
                db.commit()
                
    @staticmethod
    def update_tax_rate(tax_rate_id: int, name: str = None, rate: float = None, is_default: bool = None):
        with SessionLocal() as db:
            tax_rate = db.query(TaxRate).filter(TaxRate.id == tax_rate_id).first()
            if tax_rate:
                if name is not None:
                    tax_rate.name = name
                if rate is not None:
                    tax_rate.rate = rate
                if is_default is not None:
                    if is_default:
                        TaxRateService.clear_default_tax_rate(db)
                    tax_rate.is_default = 1 if is_default else 0
                db.commit()
                db.refresh(tax_rate)
                return tax_rate
