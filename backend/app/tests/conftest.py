import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture(scope='session')
def app():
    application = create_app('testing')
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function', autouse=True)
def clean_db(app):
    """Truncate all tables between tests."""
    yield
    with app.app_context():
        _db.session.rollback()
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


# ── Helpers ────────────────────────────────────────────────────────────────

def register_user(client, email='test@example.com', password='password123', full_name='Test User'):
    return client.post('/api/auth/register', json={
        'email': email, 'password': password, 'full_name': full_name,
    })


def login_user(client, email='test@example.com', password='password123') -> str:
    resp = client.post('/api/auth/login', json={'email': email, 'password': password})
    return resp.get_json()['data']['access_token']


def auth_headers(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}


def create_application(client, token: str, company: str = 'Acme Corp', role: str = 'Engineer'):
    return client.post('/api/applications', json={
        'company_name': company,
        'role_title': role,
        'applied_date': '2025-01-15',
    }, headers=auth_headers(token))
