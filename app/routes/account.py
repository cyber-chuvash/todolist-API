import flask
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User


class AccountAPI(MethodView):
    def get(self):
        """
        Get current user's account
        Will be implemented after some basic auth is made

        :return: HTTP 200: User account info
        :return: HTTP 401: Login required

        https://docs.todo.chuvash.pw/#/account/get_account_
        """
        raise NotImplementedError

    def post(self):
        """
        Register a new user account

        :return: HTTP 200: Successfully created a new user account: Account object

        https://docs.todo.chuvash.pw/#/account/post_account_
        """
        req = flask.request
        data = req.get_json(silent=True)
        if data is None:
            return {'error': 'Only JSON data is supported'}, 400

        if not ('username' in data and 'email' in data):
            return {'error': 'username and email are required'}, 400

        # TODO additional checks of course

        s = db.Session()
        try:
            new_user = User(username=data['username'], email=data['email'])
            s.add(new_user)
            s.commit()
        except IntegrityError:
            return {'error': "User with this email already exists"}, 409

        return flask.jsonify(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email
        )

    def delete(self):
        """
        Completely delete current users account with all of the lists associated with it.

        :return: HTTP 200: The account was successfully deleted

        https://docs.todo.chuvash.pw/#/account/delete_account_
        """
        raise NotImplementedError
