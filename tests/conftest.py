import pytest

import app
from app import db


@pytest.fixture
def flask_app(monkeypatch):
    monkeypatch.setenv("TODOLIST_APP_ENV", "test")
    yield app
    # Reset db.Session so that test_db_init works properly
    # regardless of test execution order
    db.Session = None


@pytest.fixture
def flask_client(flask_app):
    yield flask_app.create_app().test_client()
