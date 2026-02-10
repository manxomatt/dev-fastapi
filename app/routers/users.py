from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.services.user_service import create_user, list_users, get_user, update_user, delete_user
from app.db.session import get_db
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(payload: UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> UserOut:
    user = create_user(db, payload.username, payload.email, payload.password)
    return user


@router.get("", response_model=list[UserOut])
def list_users_endpoint(db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> list[UserOut]:
    return list_users(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> UserOut:
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)) -> UserOut:
    user = update_user(db, user_id, username=payload.username, email=payload.email, password=payload.password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    ok = delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
