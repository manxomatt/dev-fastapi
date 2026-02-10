from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import get_db
from app.services.user_service import get_user, find_user_by_username_or_email
from app.core.security import create_access_token, create_refresh_token, verify_token, revoke_refresh_token, is_refresh_token_revoked
from app.services.user_service import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenOut)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm provides username & password fields
    user = find_user_by_username_or_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # verify password using bcrypt
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    return TokenOut(access_token=access, refresh_token=refresh)


class RefreshIn(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=TokenOut)
def refresh(payload: RefreshIn):
    token = payload.refresh_token
    if is_refresh_token_revoked(token):
        raise HTTPException(status_code=401, detail="Refresh token revoked")
    data = verify_token(token)
    if not data or data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    sub = data.get("sub")
    access = create_access_token(sub)
    refresh = create_refresh_token(sub)
    return TokenOut(access_token=access, refresh_token=refresh)


class LogoutIn(BaseModel):
    refresh_token: str


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: LogoutIn):
    token = payload.refresh_token
    revoke_refresh_token(token)
    return None
