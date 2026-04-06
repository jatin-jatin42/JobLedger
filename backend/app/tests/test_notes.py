from .conftest import register_user, login_user, auth_headers, create_application


def _setup(client, email='test@example.com'):
    register_user(client, email=email)
    token = login_user(client, email=email)
    app_id = create_application(client, token).get_json()['data']['id']
    return token, app_id


def test_add_note_to_own_application(client):
    token, app_id = _setup(client)
    resp = client.post(f'/api/applications/{app_id}/notes',
                       json={'content': 'Spoke to recruiter'},
                       headers=auth_headers(token))
    assert resp.status_code == 201
    data = resp.get_json()['data']
    assert data['content'] == 'Spoke to recruiter'
    assert data['application_id'] == app_id


def test_add_note_to_other_users_application(client):
    token1, app_id = _setup(client, 'user1@test.com')
    register_user(client, email='user2@test.com')
    token2 = login_user(client, email='user2@test.com')
    resp = client.post(f'/api/applications/{app_id}/notes',
                       json={'content': 'Unauthorized note'},
                       headers=auth_headers(token2))
    assert resp.status_code == 404


def test_add_empty_note(client):
    token, app_id = _setup(client)
    resp = client.post(f'/api/applications/{app_id}/notes',
                       json={'content': ''},
                       headers=auth_headers(token))
    assert resp.status_code == 400


def test_add_whitespace_only_note(client):
    token, app_id = _setup(client)
    resp = client.post(f'/api/applications/{app_id}/notes',
                       json={'content': '   \t\n  '},
                       headers=auth_headers(token))
    assert resp.status_code == 400


def test_get_notes(client):
    token, app_id = _setup(client)
    client.post(f'/api/applications/{app_id}/notes',
                json={'content': 'Note 1'}, headers=auth_headers(token))
    client.post(f'/api/applications/{app_id}/notes',
                json={'content': 'Note 2'}, headers=auth_headers(token))
    resp = client.get(f'/api/applications/{app_id}/notes', headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.get_json()['total'] == 2


def test_delete_note(client):
    token, app_id = _setup(client)
    note_id = client.post(
        f'/api/applications/{app_id}/notes',
        json={'content': 'To be deleted'},
        headers=auth_headers(token),
    ).get_json()['data']['id']

    resp = client.delete(f'/api/applications/{app_id}/notes/{note_id}',
                         headers=auth_headers(token))
    assert resp.status_code == 204


def test_delete_note_wrong_user(client):
    token1, app_id = _setup(client, 'user1@test.com')
    register_user(client, email='user2@test.com')
    token2 = login_user(client, email='user2@test.com')

    note_id = client.post(
        f'/api/applications/{app_id}/notes',
        json={'content': 'Legit note'},
        headers=auth_headers(token1),
    ).get_json()['data']['id']

    resp = client.delete(f'/api/applications/{app_id}/notes/{note_id}',
                         headers=auth_headers(token2))
    assert resp.status_code == 404
