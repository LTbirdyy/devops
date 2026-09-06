import os

# Precisa ser definido ANTES de importar a app, para o cache.py usar fakeredis
os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./test_ci.db"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db

# Banco de teste isolado, recriado a cada sessão de testes
TEST_DATABASE_URL = "sqlite:///./test_ci.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("test_ci.db"):
        os.remove("test_ci.db")


@pytest.fixture()
def client():
    return TestClient(app)
