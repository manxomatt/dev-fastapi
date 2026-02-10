import sys
from sqlalchemy import create_engine, text
from app.core.config import DATABASE_URL

print("Using DATABASE_URL:", DATABASE_URL)

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Connection successful")
except Exception as e:
    print("Connection failed:", repr(e))
    sys.exit(1)
