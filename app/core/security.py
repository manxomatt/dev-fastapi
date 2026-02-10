from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.db.session import SessionLocal
from app.models.revoked_token import RevokedToken


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": subject, "exp": expire, "type": "access"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def revoke_refresh_token(token: str) -> None:
    db = SessionLocal()
    try:
        exists = db.query(RevokedToken).filter(RevokedToken.token == token).first()
        if not exists:
            db.add(RevokedToken(token=token))
            db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def is_refresh_token_revoked(token: str) -> bool:
    db = SessionLocal()
    try:
        return db.query(RevokedToken).filter(RevokedToken.token == token).first() is not None
    finally:
        db.close()
