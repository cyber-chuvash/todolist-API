

#################
#  GET /lists/  #
#################

def test_get_lists_new_user(flask_client, user_account):
    res = flask_client.get('/lists/', headers=[user_account.auth_header])
    assert res.status_code == 200

    data = res.get_json()
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_lists_created_with_fixture(flask_client, get_user_with_lists):
    num_of_lists = 3
    user = get_user_with_lists(num_of_lists)

    res = flask_client.get('/lists/', headers=[user.auth_header])
    assert res.status_code == 200

    data = res.get_json()
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == num_of_lists
    # Sort the lists and compare them
    assert sorted(user.lists, key=lambda x: x['title']) == sorted(data, key=lambda x: x['title'])


def test_get_lists_with_limit_and_offset(flask_client, get_user_with_lists):
    num_of_lists = 3
    user = get_user_with_lists(num_of_lists)

    limit = 1
    offset = 1
    res = flask_client.get('/lists/',
                           headers=[user.auth_header],
                           query_string={
                               "limit": limit,
                               "offset": offset
                           })
    assert res.status_code == 200

    data = res.get_json()
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == limit
    # Filter user.lists for the one that was returned, thus making sure that we got one of user.lists
    assert len(list(filter(lambda x: x['id'] == data[0]['id'], user.lists))) == 1


def test_get_all_lists_with_offsets(flask_client, get_user_with_lists):
    num_of_lists = 5
    user = get_user_with_lists(num_of_lists)

    returned_lists = []

    # Get first 2 lists
    first_two = flask_client.get('/lists/',
                                 headers=[user.auth_header],
                                 query_string={
                                     "limit": 2
                                 })
    assert first_two.status_code == 200
    returned_lists += first_two.get_json()

    # Get the third list
    third = flask_client.get('/lists/',
                             headers=[user.auth_header],
                             query_string={
                                 "offset": 2,
                                 "limit": 1
                             })
    assert third.status_code == 200
    returned_lists += third.get_json()

    # Get the fourth and fifth lists
    last_two = flask_client.get('/lists/',
                                headers=[user.auth_header],
                                query_string={
                                    "offset": 3,
                                    "limit": 2
                                })
    assert last_two.status_code == 200
    returned_lists += last_two.get_json()

    assert len(returned_lists) == num_of_lists
    # Sort the lists and compare them
    assert sorted(user.lists, key=lambda x: x['title']) == sorted(returned_lists, key=lambda x: x['title'])


def test_get_lists_include_cards(flask_client, get_user_with_lists):
    user = get_user_with_lists(3)
    res = flask_client.get('/lists/',
                           headers=[user.auth_header],
                           query_string={
                               "limit": 1,
                               "include_cards": True
                           })
    assert res.status_code == 200

    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0].get('id') is not None
    assert data[0].get('title') is not None
    assert isinstance(data[0].get('cards'), list)


def test_get_lists_nonexistent_user(flask_client):
    res = flask_client.get('/lists/', headers=[('Authorization', 'Bearer 1337322696969')])
    assert res.status_code == 200

    data = res.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_get_lists_no_auth(flask_client):
    res = flask_client.get('/lists/')
    assert res.status_code == 401


##################
#  POST /lists/  #
##################

def test_create_list(flask_client, user_account):
    todo_list = {
        "title": "TODO-list app TODO"
    }
    res = flask_client.post('/lists/', json=todo_list, headers=[user_account.auth_header])
    assert res.status_code == 200

    data = res.get_json()
    assert data is not None
    assert data.get('id') is not None
    assert data.get('title') == todo_list['title']


def test_create_list_rejects_urlencoded(flask_client, user_account):
    res = flask_client.post(
        '/lists/',
        data={"title": "TODO-list app TODO"},
        headers=[user_account.auth_header]
    )

    assert res.status_code == 400
    err_data = res.get_json()
    assert "error" in err_data
    assert "json" in err_data['error'].lower()
    assert "supported" in err_data['error'].lower()


def test_create_list_empty_body(flask_client, user_account):
    res = flask_client.post('/lists/', headers=[user_account.auth_header])

    assert res.status_code == 400
    assert "error" in res.get_json()


def test_create_list_no_title(flask_client, user_account):
    todo_list = {}
    res = flask_client.post('/lists/', json=todo_list, headers=[user_account.auth_header])
    assert res.status_code == 400

    data = res.get_json()
    assert data is not None
    assert data.get('error') is not None
    assert "title" in data['error'].lower()
    assert "required" in data['error'].lower()


def test_create_list_no_auth(flask_client):
    res = flask_client.post('/lists/', json={'title': 'a'})
    assert res.status_code == 401


##########################
#  GET /lists/{list_id}  #
##########################


############################
#  PATCH /lists/{list_id}  #
############################


#############################
#  DELETE /lists/{list_id}  #
#############################
