import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_db
from app.main import create_app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def client():
    # ensure models are imported so metadata is populated
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
    app = create_app()
    # seed a user directly into the test DB so we can obtain an access token
    from app.services.user_service import create_user as svc_create_user, find_user_by_username_or_email
    db_for_seed = TestingSessionLocal()
    try:
        existing = find_user_by_username_or_email(db_for_seed, "seeduser")
        if not existing:
            svc_create_user(db_for_seed, "seeduser", "seed@example.com", "seedpass")
    finally:
        db_for_seed.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # ensure tables exist in the app's engine as well
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c


def test_user_crud(client: TestClient):
    # login to get access token
    login = client.post("/auth/login", data={"username": "seeduser", "password": "seedpass"})
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create
    resp = client.post("/users", json={"username": "tuser", "email": "tuser@example.com", "password": "pass"}, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    uid = data["id"]
    assert data["username"] == "tuser"

    # get
    resp = client.get(f"/users/{uid}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "tuser@example.com"

    # list
    resp = client.get("/users", headers=headers)
    assert resp.status_code == 200
    assert any(u["username"] == "tuser" for u in resp.json())

    # update
    resp = client.put(f"/users/{uid}", json={"username": "tuser2"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "tuser2"

    # delete
    resp = client.delete(f"/users/{uid}", headers=headers)
    assert resp.status_code == 204

    # ensure gone
    resp = client.get(f"/users/{uid}", headers=headers)
    assert resp.status_code == 404
