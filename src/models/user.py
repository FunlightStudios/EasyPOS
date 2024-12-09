from sqlalchemy import Column, Integer, String, Boolean
from src.database.database import Base
import bcrypt

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)  # admin, cashier, manager

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode(), salt)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password)
