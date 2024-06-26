import pytest
from pathlib import Path
from flaskr.db import get_db
from flaskr.models.car_model import delete_car

@pytest.mark.parametrize(("car", "image"), (
    (b"Toyota Camry 2019", b"https://example.com/toyota_camry.jpg"),
    (b"Honda Civic 2020", b"https://example.com/honda_civic.jpg"),
    (b"Ford Mustang 2018", b"https://example.com/ford_mustang.jpg"),
))
def test_index_regular_user(client, car, image):
    response = client.get("/")
    print(response.data)
    assert response.status_code == 200
    assert car in response.data
    assert image in response.data

def test_index_admin(client, auth):
    auth.login()
    response = client.get('/')
    assert b'Gerenciar' in response.data
    assert b'Adicionar' in response.data

def test_admin_logout(client, auth):
    auth.login()
    response = client.get('/')
    assert b'Gerenciar' in response.data

    auth.logout()
    response = client.get('/')
    assert b'Gerenciar' not in response.data

@pytest.mark.parametrize('path', ('/car/4/edit', '/car/4/delete'))
def test_valid_car_required(auth, client, path):
    auth.login()
    client.post(path).status_code == 404

# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"
def test_create_car(auth, client, app):
    auth.login()
    client.post('/car/create', data = {
        'make': 'Ford', 'model': 'Fusion', 'year': 2020, 'fuel_type': 'Gasolina', 'price': 120000,
        'pictures': (resources / "car.jpg").open("rb"),
    })

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM car WHERE id = 4').fetchone()
        assert post['make'] == 'Ford'
        assert post['model'] == 'Fusion'
        delete_car(4)

def test_update(auth, client, app):
    auth.login()
    client.post('/car/3/edit', data = {
        'make': 'Ford', 'model': 'Fusion', 'year': 2020, 'fuel_type': 'Gasolina', 'price': 120000
    })
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM car WHERE id = 3').fetchone()
        assert post['make'] == 'Ford'
        assert post['model'] == 'Fusion'

def test_delete(auth, client, app):
    auth.login()
    client.post('/car/create', data = {
        'make': 'Ford', 'model': 'Fusion', 'year': 2020, 'fuel_type': 'Gasolina', 'price': 120000,
        'pictures': (resources / "car.jpg").open("rb"),
    })

    response = client.post('car/4/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM car WHERE id = 4').fetchone()
        assert post is None