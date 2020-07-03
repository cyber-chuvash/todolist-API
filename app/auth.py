from flask import g, request


def auth_required(f):
    """
    Decorates f to authenticate the request with a simple bearer token.
    For now token == user_id.

    :param f: function: Flask view function to decorate
    :return: HTTP 401: Authentication required, but none provided
    :return: HTTP 400: Header is malformed, contains unsupported token type or malformed token
    :return: Result of calling f() if request was authenticated
    """
    def _auth(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return {"error": "Authentication is required"}, 401, \
                   {'WWW-Authenticate': 'Bearer realm="api.todo.chuvash.pw"'}

        try:
            token_type, token = auth_header.split(' ')[:2]
        except ValueError:
            return {"error": "Authorization header is malformed"}, 400

        if token_type.lower() != 'bearer':
            return {"error": "Only Bearer tokens are supported"}, 400

        g.auth = {'user_id': token}

        return f(*args, **kwargs)

    return _auth

