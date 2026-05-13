"""Integration tests for the task-manager-api.

Each test gets a fresh in-memory SQLite database via dependency override so tests
don't share state and don't touch the on-disk dev database (`tasks.db`).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from database import Base
from main import app, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_task_returns_id(client):
    resp = client.post("/tasks", json={"title": "buy milk"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "buy milk"
    assert body["is_completed"] is False
    assert "id" in body and isinstance(body["id"], int)


def test_list_tasks_after_create(client):
    client.post("/tasks", json={"title": "a"})
    client.post("/tasks", json={"title": "b"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    titles = [t["title"] for t in resp.json()]
    assert titles == ["a", "b"]


def test_filter_tasks_by_title(client):
    client.post("/tasks", json={"title": "buy milk"})
    client.post("/tasks", json={"title": "walk dog"})
    resp = client.get("/tasks", params={"title": "milk"})
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    assert resp.json()[0]["title"] == "buy milk"


def test_get_unknown_task_returns_404(client):
    assert client.get("/tasks/999").status_code == 404


def test_update_task(client):
    task_id = client.post("/tasks", json={"title": "old"}).json()["id"]
    resp = client.put(
        f"/tasks/{task_id}",
        json={"title": "new", "description": "now with detail", "is_completed": True},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["title"] == "new"
    assert body["is_completed"] is True


def test_delete_task(client):
    task_id = client.post("/tasks", json={"title": "doomed"}).json()["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 200
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_unknown_task_returns_404(client):
    assert client.delete("/tasks/999").status_code == 404
