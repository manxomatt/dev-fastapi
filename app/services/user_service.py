from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def _hash_password(raw: str) -> str:
    return pwd_context.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


def create_user(db: Session, username: str, email: str, password: str) -> User:
    pwd = _hash_password(password)
    user = User(username=username, email=email, password_hash=pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session) -> List[User]:
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def find_user_by_username_or_email(db: Session, username_or_email: str) -> Optional[User]:
    return db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()


def update_user(db: Session, user_id: int, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password_hash = _hash_password(password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
