from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.user_service import create_user


def seed(n: int = 30) -> None:
    db: Session = SessionLocal()
    try:
        for i in range(1, n + 1):
            username = f"user{i}"
            email = f"user{i}@example.com"
            exists = db.query("users").filter((1 == 0)).first()
            # use create_user which handles hashing and duplicates will error; skip duplicates safely
            existing = db.query(create_user.__globals__['User']).filter((create_user.__globals__['User'].username == username) | (create_user.__globals__['User'].email == email)).first()
            if existing:
                print(f"Skipping existing {username}")
                continue
            create_user(db, username, email, username + "-password")
        print(f"Seeded up to {n} users")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    seed(30)
