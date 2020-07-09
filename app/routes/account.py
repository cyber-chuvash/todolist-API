import flask
from flask import g
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.user import User
from app.auth import auth_required


class AccountAPI(MethodView):
    @auth_required
    def get(self):
        """
        Get current user's account

        :return: HTTP 200: User account info

        https://docs.todo.chuvash.pw/#/account/get_account_
        """
        s = db.Session()
        try:
            account = s.query(User).filter_by(id=g.auth['user_id']).one()
        except NoResultFound:
            return {'error': 'Account not found'}, 404

        return account.get_api_repr(include_email=True)

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

        return new_user.get_api_repr(include_email=True)

    @auth_required
    def delete(self):
        """
        Completely delete current users account with all of the lists associated with it.

        :return: HTTP 200: The account was successfully deleted

        https://docs.todo.chuvash.pw/#/account/delete_account_
        """

        s = db.Session()
        try:
            account_to_delete = s.query(User).filter_by(id=g.auth['user_id']).one()
            s.delete(account_to_delete)
            s.commit()
        except NoResultFound:
            return {'error': "Account was already deleted"}, 404

        return 'ok', 200

