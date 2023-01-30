from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db import database
import db.database
import api.main as main

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


db.database.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

main.app.dependency_overrides[main.get_db] = override_get_db

client = TestClient(main.app)

def test_add_city(city_name):
    response = client.post(f"/weather/{city_name}")
    assert response.status_code == 200, response.text
    data = response.json()
    print(data)


if __name__ == '__main__':
    test_add_city('Obninsk')