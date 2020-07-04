import pytest

import app
from app import db


def test_db_init(flask_app):
    assert db.Session is None
    a = flask_app.create_app()
    assert db.Session is not None


def test_db_teardown_ctx(flask_app):
    a = flask_app.create_app()
    # Probable false-positive, if other teardown context funcs were added
    assert len(a.teardown_appcontext_funcs) > 0

    # Possible false-negative, if name of the func was changed
    assert 'shutdown_db_session' in map(lambda x: x.__name__, a.teardown_appcontext_funcs)


def test_config_with_good_env(monkeypatch):
    # Test env with good value
    monkeypatch.setenv("TODOLIST_APP_ENV", "test")
    _ = app.create_app()


def test_config_raises_on_bad_env(monkeypatch):
    # Test empty env
    with pytest.raises(ValueError):
        _ = app.create_app()

    # Test env with bad value
    monkeypatch.setenv("TODOLIST_APP_ENV", "badvalue")
    with pytest.raises(ValueError):
        _ = app.create_app()


def test_get_404(flask_client):
    res = flask_client.get('/non-existent/route/blahblahblah/can/has/404/?')
    assert res.status_code == 404

