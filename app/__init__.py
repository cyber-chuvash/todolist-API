from flask import Flask

from app import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is not None:
        app.config.from_mapping(test_config)

    @app.teardown_appcontext
    def shutdown_db_session(exc=None):
        db.Session.remove()

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app
