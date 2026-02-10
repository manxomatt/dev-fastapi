from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.item import Item


def create_item(db: Session, name: str) -> Item:
    db_item = Item(name=name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def list_items(db: Session) -> List[Item]:
    return db.query(Item).all()


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

