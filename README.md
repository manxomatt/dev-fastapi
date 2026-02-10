Quick setup

1. Create virtual env and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create a `.env` file (or use `.env.example`) to set `DATABASE_URL`.

3. Initialize and run Alembic migrations:

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

4. Run the app:

```bash
uvicorn app.main:app --reload
```

MySQL notes

- Ensure MySQL server is running and a database named `dev_py` exists. Example using `mysql` CLI:

```bash
# create database (run as root or a user with privileges)
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS dev_py;"
```

- The project uses `pymysql` driver. It's included in `requirements.txt`.
- To use the provided MySQL credentials, a `.env` file with the following is used:

```text
DATABASE_URL=mysql+pymysql://root:password@localhost/dev_py
```

- Then run migrations and start the app as above.
