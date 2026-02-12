from typing import List, Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.repositories import user_repository


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


def create_user(db: Session, username: str, email: str, password: str) -> User:
    pwd = _hash_password(password)
    return user_repository.create(db, username, email, pwd)


def list_users(db: Session) -> List[User]:
    return user_repository.list_all(db)


def get_user(db: Session, user_id: int) -> Optional[User]:
    return user_repository.get_by_id(db, user_id)


def find_user_by_username_or_email(db: Session, username_or_email: str) -> Optional[User]:
    return user_repository.find_by_username_or_email(db, username_or_email)


def update_user(db: Session, user_id: int, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    pwd_hash = _hash_password(password) if password else None
    return user_repository.update(db, user, username=username, email=email, password_hash=pwd_hash)


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    user_repository.delete(db, user)
    return True
