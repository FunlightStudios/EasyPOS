from src.models.user import User
from src.database.database import SessionLocal
import bcrypt

class AuthService:
    @staticmethod
    def create_user(username: str, password: str, email: str, role: str = "cashier"):
        with SessionLocal() as db:
            user = User(
                username=username,
                email=email,
                role=role
            )
            user.set_password(password)
            db.add(user)
            db.commit()
            return user

    @staticmethod
    def authenticate_user(username: str, password: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            if user and user.check_password(password):
                return user
            return None

    @staticmethod
    def get_user(user_id: int):
        with SessionLocal() as db:
            return db.query(User).filter(User.id == user_id).first()
