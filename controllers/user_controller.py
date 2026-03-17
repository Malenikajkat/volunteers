from database.db import SessionLocal
from models.user import User
from utils.validation import validate_email, validate_phone, validate_name
import hashlib


class UserController:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(full_name, email, phone, password):
        if not all([validate_name(full_name), validate_email(email), validate_phone(phone)]):
            return False, "Некорректные данные"

        hashed = UserController.hash_password(password)
        db = SessionLocal()
        try:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return False, "Пользователь с такой почтой уже существует"

            new_user = User(
                full_name=full_name,
                email=email,
                phone=phone,
                password=hashed
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return True, "Регистрация успешна"
        except Exception as e:
            db.rollback()
            return False, f"Ошибка базы данных: {e}"
        finally:
            db.close()

    @staticmethod
    def login(email, password):
        if not validate_email(email):
            return False, "Неверный формат email"

        hashed = UserController.hash_password(password)
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email, User.password == hashed).first()
            if user:
                return True, user
            return False, "Неверный логин или пароль"
        finally:
            db.close()