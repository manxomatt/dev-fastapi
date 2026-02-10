from sqlalchemy import create_engine, inspect
from app.core.config import DATABASE_URL

print("Using DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
print("Tables:", inspector.get_table_names())
