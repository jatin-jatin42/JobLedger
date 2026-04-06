from .conftest import register_user, login_user, auth_headers, create_application


def _setup(client, email='test@example.com'):
    register_user(client, email=email)
    return login_user(client, email=email)


def test_create_application_valid(client):
    token = _setup(client)
    resp = create_application(client, token)
    assert resp.status_code == 201
    data = resp.get_json()['data']
    assert data['company_name'] == 'Acme Corp'
    assert data['stage'] == 'APPLIED'


def test_create_application_missing_required(client):
    token = _setup(client)
    resp = client.post('/api/applications',
                       json={'role_title': 'Engineer'},
                       headers=auth_headers(token))
    assert resp.status_code == 400


def test_create_application_salary_invalid(client):
    token = _setup(client)
    resp = client.post('/api/applications', json={
        'company_name': 'Corp', 'role_title': 'Eng',
        'salary_min': 100, 'salary_max': 50, 'applied_date': '2025-01-15',
    }, headers=auth_headers(token))
    assert resp.status_code == 422


def test_create_application_future_date(client):
    token = _setup(client)
    resp = client.post('/api/applications', json={
        'company_name': 'Corp', 'role_title': 'Eng', 'applied_date': '2099-01-01',
    }, headers=auth_headers(token))
    assert resp.status_code == 422


def test_list_applications_only_own(client):
    token1 = _setup(client, 'user1@test.com')
    token2 = _setup(client, 'user2@test.com')
    create_application(client, token1, company='User1Corp')
    create_application(client, token2, company='User2Corp')

    resp = client.get('/api/applications', headers=auth_headers(token1))
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload['total'] == 1
    assert payload['data'][0]['company_name'] == 'User1Corp'


def test_get_application_by_id(client):
    token = _setup(client)
    app_id = create_application(client, token).get_json()['data']['id']
    resp = client.get(f'/api/applications/{app_id}', headers=auth_headers(token))
    assert resp.status_code == 200
    assert 'notes' in resp.get_json()['data']


def test_get_other_users_application(client):
    token1 = _setup(client, 'user1@test.com')
    token2 = _setup(client, 'user2@test.com')
    app_id = create_application(client, token1).get_json()['data']['id']
    resp = client.get(f'/api/applications/{app_id}', headers=auth_headers(token2))
    assert resp.status_code == 404


def test_update_application(client):
    token = _setup(client)
    app_id = create_application(client, token).get_json()['data']['id']
    resp = client.patch(f'/api/applications/{app_id}',
                        json={'company_name': 'Updated Corp'},
                        headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.get_json()['data']['company_name'] == 'Updated Corp'


def test_update_does_not_change_stage(client):
    """PATCH /applications/:id must not modify stage."""
    token = _setup(client)
    app_id = create_application(client, token).get_json()['data']['id']
    client.patch(f'/api/applications/{app_id}',
                 json={'stage': 'OFFER'},
                 headers=auth_headers(token))
    resp = client.get(f'/api/applications/{app_id}', headers=auth_headers(token))
    assert resp.get_json()['data']['stage'] == 'APPLIED'


def test_delete_application(client):
    token = _setup(client)
    app_id = create_application(client, token).get_json()['data']['id']
    resp = client.delete(f'/api/applications/{app_id}', headers=auth_headers(token))
    assert resp.status_code == 204


def test_delete_other_users_application(client):
    token1 = _setup(client, 'user1@test.com')
    token2 = _setup(client, 'user2@test.com')
    app_id = create_application(client, token1).get_json()['data']['id']
    resp = client.delete(f'/api/applications/{app_id}', headers=auth_headers(token2))
    assert resp.status_code == 404
