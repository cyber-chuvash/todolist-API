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

        return user.get_api_repr(include_email=False)
