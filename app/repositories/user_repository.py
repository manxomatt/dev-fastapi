from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User


def create(db: Session, username: str, email: str, password_hash: str) -> User:
    user = User(username=username, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_all(db: Session) -> List[User]:
    return db.query(User).all()


def get_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def find_by_username_or_email(db: Session, username_or_email: str) -> Optional[User]:
    return db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()


def update(db: Session, user: User, username: str | None = None, email: str | None = None, password_hash: str | None = None) -> User:
    if username:
        user.username = username
    if email:
        user.email = email
    if password_hash:
        user.password_hash = password_hash
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()
