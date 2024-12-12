import pytest
import os
from flask_jwt_extended import create_access_token
from admin.src.extensions import db
from admin.src.model.AdminsModel import Admin
from admin.app import create_app

@pytest.fixture
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_token(app):
    with app.app_context():
        admin = Admin(
            username='testadmin',
            email='admin@test.com',
            first_name='Test',
            last_name='Admin',
            phone='12345678',
            age=30,
            gender='male',
            marital_status='single'
        )
        admin.set_password('password123')
        db.session.add(admin)
        db.session.commit()
        token = create_access_token(identity=admin.username)
        return token

def test_register_admin(client):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "johndoe@example.com",
        "phone": "12345678",
        "age": 25,
        "gender": "male",
        "marital_status": "single"
    }
    response = client.put('/admin/register_admin', json=payload)
    assert response.status_code == 201
    assert response.json['access']
    assert response.json['refresh']

def test_login_admin(client, admin_token):
    payload = {
        "identifier": "testadmin",
        "password": "password123"
    }
    response = client.post('/admin/login_admin', json=payload)
    assert response.status_code == 200
    assert response.json['access']
    assert response.json['refresh']

def test_update_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    payload = {
        "first_name": "Updated",
        "last_name": "Updated",
        "phone": "87654321"
    }
    response = client.put('/admin/update_admin', json=payload, headers=headers)
    print(response.json)
    assert response.status_code == 200
    assert response.json['message'] == "Admin updated successfully"

def test_logout_admin(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.delete('/admin/logout_admin', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Admin logged out successfully"

def test_get_admin_info(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.get('/admin/get_admin_info', headers=headers)
    print(response.json)
    assert response.status_code == 200
    assert "username" in response.json
    assert response.json["username"] == "testadmin"


@pytest.mark.parametrize("duplicate_field,value", [
    ("username", "testadmin"),
    ("email", "admin@test.com"),
    ("phone", "12345678")
])
def test_register_admin_duplicate_fields(client, admin_token, duplicate_field, value):
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "uniqueuser",
        "password": "password123",
        "email": "unique@example.com",
        "phone": "87654321",
        "age": 25,
        "gender": "male",
        "marital_status": "single"
    }
    payload[duplicate_field] = value
    
    response = client.put('/admin/register_admin', json=payload)
    assert response.status_code == 408
    assert 'error' in response.json

def test_get_admin_info_nonexistent(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    with client.application.app_context():
        admin = Admin.query.filter_by(username='testadmin').first()
        if admin:
            db.session.delete(admin)
            db.session.commit()

    response = client.get('/admin/get_admin_info', headers=headers)
    assert response.status_code == 404
    assert 'error' in response.json

def test_get_admin_info_no_token(client):
    response = client.get('/admin/get_admin_info')
    assert response.status_code == 401
    assert 'msg' in response.json
    assert "missing authorization header" in response.json['msg'].lower()
