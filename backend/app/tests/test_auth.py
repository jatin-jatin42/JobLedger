from .conftest import register_user, login_user, auth_headers


def test_register_valid(client):
    resp = register_user(client)
    assert resp.status_code == 201
    data = resp.get_json()['data']
    assert data['email'] == 'test@example.com'
    assert 'password' not in data
    assert 'password_hash' not in data


def test_register_duplicate_email(client):
    register_user(client)
    resp = register_user(client)
    assert resp.status_code == 409


def test_register_missing_fields(client):
    resp = client.post('/api/auth/register', json={'email': 'a@b.com'})
    assert resp.status_code == 400


def test_register_missing_email(client):
    resp = client.post('/api/auth/register', json={'password': 'pass1234', 'full_name': 'Bob'})
    assert resp.status_code == 400


def test_register_weak_password(client):
    resp = client.post('/api/auth/register', json={
        'email': 'a@b.com', 'password': 'short', 'full_name': 'Test User',
    })
    assert resp.status_code == 400


def test_register_invalid_email_format(client):
    resp = client.post('/api/auth/register', json={
        'email': 'not-an-email', 'password': 'password123', 'full_name': 'Test',
    })
    assert resp.status_code == 400


def test_login_valid(client):
    register_user(client)
    resp = client.post('/api/auth/login', json={
        'email': 'test@example.com', 'password': 'password123',
    })
    assert resp.status_code == 200
    data = resp.get_json()['data']
    assert 'access_token' in data
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'


def test_login_wrong_password(client):
    register_user(client)
    resp = client.post('/api/auth/login', json={
        'email': 'test@example.com', 'password': 'wrongpass',
    })
    assert resp.status_code == 401


def test_login_nonexistent_email(client):
    resp = client.post('/api/auth/login', json={
        'email': 'nobody@example.com', 'password': 'password123',
    })
    assert resp.status_code == 401
    # Same error message as wrong password — no email enumeration
    assert 'Invalid' in resp.get_json()['error']


def test_me_without_token(client):
    resp = client.get('/api/auth/me')
    assert resp.status_code == 401


def test_me_with_valid_token(client):
    register_user(client)
    token = login_user(client)
    resp = client.get('/api/auth/me', headers=auth_headers(token))
    assert resp.status_code == 200
    assert resp.get_json()['data']['email'] == 'test@example.com'
