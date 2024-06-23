import pytest
from flask import g, session
from flaskr.models.auth_model import get_user_by_username

def test_register(client, app):
    data = {'username': 'user', 'password': 'pass'}
    assert client.get('/auth/register').status_code == 200

    response = client.post(
        '/auth/register',
        data=data
    )
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        user = get_user_by_username(data['username'])
    assert user is not None
    assert user['username'] == data['username']

@pytest.mark.parametrize(("username", "password", "message"), (
    ('', '', b'Username is required.'),
    ('nopassword', '', b'Password is required.'),
    ('user1', 'password1', b'is already registered.'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert g.user['username'] == 'user1'
        assert session['user_id'] == 1