import os

from flask import Flask

from app import db
from app.routes.users import UserAPI
from app.routes.account import AccountAPI


envs = {
    "dev": "../configs/dev.py",
    "test": "../configs/test.py",
    "prod": "ENVIRON"
}


def configure(app):
    env = os.environ.get('TODOLIST_APP_ENV', None)
    if env not in envs.keys():
        raise ValueError(f'TODOLIST_APP_ENV env var MUST be set to one of {", ".join(envs.keys())}')

    if envs[env] == 'ENVIRON':
        app.config.from_envvar("TODOLIST_APP_CONFIG_FILE")
    else:
        app.config.from_pyfile(envs[env])


def register_route(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def create_app():
    app = Flask(__name__)
    configure(app)
    db.init_db(app)

    @app.teardown_appcontext
    def shutdown_db_session(exc=None):
        db.Session.remove()

    register_route(app, UserAPI, 'user_api', '/users/', 'user_id')

    account_view = AccountAPI.as_view('account_api')
    app.add_url_rule('/account/', view_func=account_view, methods=['GET', 'POST', 'DELETE', 'PATCH'])

    return app
