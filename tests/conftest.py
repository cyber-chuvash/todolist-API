import random
import string

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


@pytest.fixture
def user_account(flask_client):
    class UserAccount:
        def __init__(self, username):
            self.username = username

            self.is_registered = False
            self.id = None

        @classmethod
        def create_random(cls):
            username = ''.join(random.choices(string.ascii_lowercase, k=8))
            return cls(username)

        @property
        def email(self):
            return f'{self.username}@gmail.com'

        @property
        def reg_repr(self):
            return {
                "username": self.username,
                "email": self.email
            }

        def register(self):
            if self.is_registered:
                raise ValueError('Account already registered')
            res = flask_client.post('/account/', json=self.reg_repr)
            self.id = res.get_json()['id']
            self.is_registered = True

        @property
        def auth_header(self):
            return 'Authorization', f'Bearer {self.id}'

    acc = UserAccount.create_random()
    acc.register()

    return acc
