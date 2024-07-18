from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
import pytest
from ..models import Todos


SQLALCHEMY_DATABASE_URL = "sqlite:///./test-db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


def override_get_current_user():
    return {"username": "admin", "id": 1, "user_role": "admin"}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learning",
        description="Learning",
        priority=4,
        complete=True,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "title": "Learning",
            "description": "Learning",
            "priority": 4,
            "complete": True,
            "owner_id": 1,
            "id": 1,
        }
    ]

