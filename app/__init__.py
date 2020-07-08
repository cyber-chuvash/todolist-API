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


def register_route(app, route, base_url, endpoint_name=None, key='id', key_type='int'):
    """
    Register a typical keyed RESTful route with add_url_rule,
    differentiating the key use between HTTP methods

    Docs on Flask route registrations:
    https://flask.palletsprojects.com/en/1.1.x/api/#url-route-registrations

    :param app: the Flask (werkzeug) app to register the route to
    :param route: the route, a class inheriting from flask.views.View
    :param base_url: URL to bind the route to, not including <the_key>
    :param endpoint_name: The endpoint name for Flask to bind the route to
    :param key: name of the key
    :param key_type: type of (converter name for) the key
    """

    endpoint_name = endpoint_name or route.__name__
    view_func = route.as_view(endpoint_name)

    # Register GET for resources without the key (i.e. id)
    app.add_url_rule(base_url, defaults={key: None},
                     view_func=view_func, methods=['GET'])

    # Register POST for resources (without the key by the REST philosophy)
    app.add_url_rule(base_url, view_func=view_func, methods=['POST'])

    # Register GET, PUT, DELETE for resources with a key of type key_type
    # Requests with other key types get 404'd
    app.add_url_rule('%s<%s:%s>' % (base_url, key_type, key), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def create_app():
    app = Flask(__name__)
    configure(app)
    db.init_db(app)

    @app.teardown_appcontext
    def shutdown_db_session(exc=None):
        db.Session.remove()

    register_route(app, UserAPI, '/users/', key='user_id')

    account_view = AccountAPI.as_view('account_api')
    app.add_url_rule('/account/', view_func=account_view, methods=['GET', 'POST', 'DELETE', 'PATCH'])

    return app
