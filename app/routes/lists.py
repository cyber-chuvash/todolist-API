import flask
from flask.views import MethodView

from app import db
from app.auth import auth_required
from app.models.todolist import List


class ListAPI(MethodView):
    @auth_required
    def get(self, list_id):
        if list_id is not None:
            return self.get_specific(list_id)
        else:
            return self.get_all()

    def get_specific(self, list_id):
        pass

    def get_all(self):
        """
        Get all lists associated with the user

        :return: HTTP 200: Array of user's lists

        https://docs.todo.chuvash.pw/#/lists/get_lists_
        """
        req = flask.request
        user_id = flask.g.auth['user_id']

        limit = int(req.args.get('limit', 20))
        offset = int(req.args.get('offset', 0))
        include_cards = req.args.get('include_cards', 'false').lower() in ('true', '1', 'yes')

        if not 0 < limit < 100:
            return {'error': 'limit must be between 0 and 100'}, 400
        if not 0 <= offset:
            return {'error': 'offset must be greater than or equal to 0'}, 400

        s = db.Session()
        user_lists = s.query(List).filter_by(owner_id=user_id)
        requested_lists = user_lists.limit(limit).offset(offset).all()

        return flask.jsonify(
            list(map(
                    lambda lst: lst.get_api_repr(include_cards=include_cards),
                    requested_lists
            ))
        )

    @auth_required
    def post(self):
        """
        Create a new list

        :return: HTTP 200: Successfully created a new list: New list object

        https://docs.todo.chuvash.pw/#/lists/post_lists_
        """
        req = flask.request
        data = req.get_json(silent=True)
        if data is None:
            return {'error': 'Only JSON data is supported'}, 400

        if 'title' not in data:
            return {'error': 'List title is required'}, 400

        s = db.Session()
        new_list = List(owner_id=flask.g.auth['user_id'], title=data['title'])
        s.add(new_list)
        s.commit()

        return new_list.get_api_repr(include_cards=False)

    def patch(self, list_id):
        pass

    def delete(self, list_id):
        pass
