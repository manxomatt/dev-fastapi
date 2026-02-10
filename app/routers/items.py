from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.item import ItemCreate, ItemOut
from app.services.item_service import create_item, list_items, get_item
from app.db.session import get_db

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=list[ItemOut], status_code=status.HTTP_201_CREATED)
def create_item_endpoint(payload: ItemCreate, db: Session = Depends(get_db)) -> list[ItemOut]:
    create_item(db, payload.name)
    items = list_items(db)
    return [ItemOut(id=item.id, name=item.name) for item in items]


@router.get("", response_model=list[ItemOut])
def list_items_endpoint(db: Session = Depends(get_db)) -> list[ItemOut]:
    items = list_items(db)
    return [ItemOut(id=item.id, name=item.name) for item in items]


@router.get("/{item_id}", response_model=ItemOut)
def get_item_endpoint(item_id: int, db: Session = Depends(get_db)) -> ItemOut:
    item = get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemOut(id=item.id, name=item.name)
