import flask
from flask.views import MethodView
from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.models.user import User


class UserAPI(MethodView):
    def get(self, user_id):
        if user_id is None:
            return {'error': 'user_id is required'}, 400

        s = db.Session()
        try:
            user = s.query(User).filter_by(id=user_id).one()
        except NoResultFound:
            return {'error': 'User not found'}, 404

        return flask.jsonify(id=user.id,
                             name=user.name)

    def post(self):
        req = flask.request
        data = req.get_json(silent=True)
        if data is None:
            return {'error': 'Only JSON data is supported'}, 400

        if not ('name' in data):
            return {'error': 'name is required'}, 400

        # TODO additional checks of course

        s = db.Session()
        new_user = User(name=data['name'])
        s.add(new_user)
        s.commit()

        return {'id': new_user.id}

    def delete(self, user_id):
        raise NotImplementedError

    def put(self, user_id):
        raise NotImplementedError
