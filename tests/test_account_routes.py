
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
