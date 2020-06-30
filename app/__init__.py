from flask import Flask

from app import db
from app.routes import users


def register_route(app, view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.teardown_appcontext
    def shutdown_db_session(exc=None):
        db.Session.remove()

    register_route(app, users.UserAPI, 'user_api', '/users/', 'user_id')

    return app
