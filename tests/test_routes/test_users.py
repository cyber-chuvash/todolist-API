

#####################
#  GET /users/{id}  #
#####################

def test_get_user(flask_client, user_account):
    res = flask_client.get(f'/users/{user_account.id}')
    data = res.get_json()
    assert res.status_code == 200

    assert data is not None
    assert data.get('error') is None

    assert data.get('id') == user_account.id
    assert data.get('username') == user_account.username


def test_get_user_empty_path(flask_client):
    res = flask_client.get('/users/')
    assert res.status_code == 400

    data = res.get_json()
    assert data.get('error') is not None
    assert "user_id" in data['error']
    assert "required" in data['error']


def test_get_user_bad_path(flask_client):
    res = flask_client.get('/users/somethingthatshouldntbehere')
    assert res.status_code == 404


def test_get_nonexistent_user(flask_client):
    res = flask_client.get('/users/1337322696969')
    assert res.status_code == 404

    data = res.get_json()
    assert data.get('error') is not None
    assert "not found" in data['error']
