

####################
#  POST /account/  #
####################

def test_create_account(flask_client):
    shrek = {
        "username": "Shrek",
        "email": "ceo@swamp.com"
    }
    res = flask_client.post('/account/', json=shrek)

    assert res.status_code == 200
    created_user = res.get_json()

    # Assert POST requests returns something in JSON
    assert created_user is not None
    # Assert that the id field is present
    assert created_user.get('id') is not None
    # Assert data didn't change
    assert created_user.get('username') == shrek['username']
    assert created_user.get('email') == shrek['email']


def test_create_account_rejects_urlencoded(flask_client):
    res = flask_client.post(
        '/account/',
        data={"username": "Donkey", "email": "donkey@swamp.com"}
    )

    assert res.status_code == 400
    err_data = res.get_json()
    assert "error" in err_data
    assert "json" in err_data['error'].lower()
    assert "supported" in err_data['error'].lower()


def test_create_account_empty_body(flask_client):
    res = flask_client.post('/account/')

    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_account_no_username(flask_client):
    user_no_name = {
        "email": "noname@swamp.com"
    }
    res = flask_client.post('/account/', json=user_no_name)

    err_data = res.get_json()
    assert res.status_code == 400
    assert "error" in err_data
    assert "username" in err_data['error']
    assert "required" in err_data['error']


def test_create_account_no_email(flask_client):
    user_no_email = {
        "username": "no-email-man"
    }
    res = flask_client.post('/account/', json=user_no_email)

    err_data = res.get_json()
    assert res.status_code == 400
    assert "error" in err_data
    assert "email" in err_data['error']
    assert "required" in err_data['error']


def test_create_account_existing_email(flask_client):
    # Create first user with this email
    donkey = {
        "username": "Donkey",
        "email": "donkey@swamp.com"
    }
    res = flask_client.post('/account/', json=donkey)

    assert res.status_code == 200

    # Try to create another user with this same email, but another name
    donkey["username"] = 'Dankey'
    res = flask_client.post('/account/', json=donkey)

    assert res.status_code == 409
    err_data = res.get_json()
    assert "error" in err_data
    assert "email" in err_data['error']
    assert "exists" in err_data['error']


######################
#   GET /account/    #
######################

def test_get_account(flask_client, user_account):
    res = flask_client.get('/account/', headers=[user_account.auth_header])
    assert res.status_code == 200

    data = res.get_json()
    assert data is not None
    assert "error" not in data

    assert data.get('id') == user_account.id
    assert data.get('email') == user_account.email
    assert data.get('username') == user_account.username


def test_get_nonexistent_account(flask_client):
    res = flask_client.get('/account/', headers=[('Authorization', 'Bearer 1337322696969')])
    assert res.status_code == 404

    data = res.get_json()
    assert "error" in data
    assert "account" in data['error'].lower()
    assert "not found" in data['error']


def test_get_account_no_auth(flask_client):
    # Basically check that we didn't forget to add @auth_required
    # Headers, error msg, etc. are covered by test_auth tests
    res = flask_client.get('/account/')
    assert res.status_code == 401


######################
#  DELETE /account/  #
######################

def test_delete_account(flask_client, user_account):
    res = flask_client.delete('/account/', headers=[user_account.auth_header])
    assert res.status_code == 200

    get_deleted_user_res = flask_client.get(f'/users/{user_account.id}')
    assert get_deleted_user_res.status_code == 404


def test_repeated_delete_account(flask_client, user_account):
    res = flask_client.delete('/account/', headers=[user_account.auth_header])
    assert res.status_code == 200

    del_again_res = flask_client.delete('/account/', headers=[user_account.auth_header])
    assert del_again_res.status_code == 404
    assert "error" in del_again_res.get_json()
    assert "already deleted" in del_again_res.get_json()['error']


def test_delete_account_no_auth(flask_client):
    res = flask_client.delete('/account/')
    assert res.status_code == 401
