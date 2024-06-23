import pytest
import tempfile
import os

from flaskr import create_app
from flaskr.db import init_db, get_db
from flaskr.models.auth_model import register_user


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'dev'
    })

    with app.app_context():
        init_db()
        register_user('user1', 'password123')
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username = 'user1', password = 'password123'):
        return self._client.post(
            '/auth/login',
            data = {'username': username, 'password': password}
        )
    def logout(self):
        return self._client.geT('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)