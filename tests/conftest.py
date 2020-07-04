import pytest

import app


@pytest.fixture
def flask_app(monkeypatch):
    monkeypatch.setenv("TODOLIST_APP_ENV", "test")
    return app


@pytest.fixture
def flask_client(flask_app):
    return flask_app.create_app().test_client()

