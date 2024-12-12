import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from admin.src.api.v1.controllers.admin_controllers import admin_bp
from shared.db import db
from shared.models.AdminsModel import Admin
from admin.config import get_config
from flask_jwt_extended import JWTManager
from admin.app import create_app 

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    JWTManager(app)  # Initialize JWTManager for tests
    with app.app_context():
        db.create_all()  # Create database tables for testing
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
        token = create_access_token(identity=str(admin.id))
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
    print(response.json)
    assert response.status_code == 200
    assert response.json['message'] == "Admin logged out successfully"

def test_get_admin_info(client, admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = client.post('/admin/get_admin_info', headers=headers)
    print(response.json)
    assert response.status_code == 200
    assert "username" in response.json
    assert response.json["username"] == "testadmin"
