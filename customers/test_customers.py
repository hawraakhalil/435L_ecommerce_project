import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from customers.app import create_app
from shared.db import db
from shared.models.CustomersModel import Customer

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()

        customer = Customer(
            username='testcustomer',
            email='customer@test.com',
            first_name='Test',
            last_name='Customer',
            phone='12345678',
            age=30,
            gender='male',
            marital_status='single'
        )
        customer.set_password('password123')
        db.session.add(customer)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def customer_token(app):
    with app.app_context():
        customer = Customer(
            username='customer',
            email='custom@test.com',
            first_name='Test',
            last_name='Customer',
            phone='12345678',
            age=30,
            gender='male',
            marital_status='single'
        )
        customer.set_password('password123')
        db.session.add(customer)
        db.session.commit()

        token = create_access_token(identity=str(customer.id))
        return token

def test_register_customer(client):
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
    response = client.put('/customers/register_customer', json=payload)
    assert response.status_code == 201
    assert response.json['access']
    assert response.json['refresh']

def test_login_customer(client):
    payload = {
        "identifier": "testcustomer",
        "password": "password123"
    }
    response = client.post('/customers/login_customer', json=payload)
    print(response.json)
    assert response.status_code == 200
    assert response.json['access']
    assert response.json['refresh']

def test_update_customer(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    payload = {
        "first_name": "Updated",
        "last_name": "Updated",
        "phone": "87654321"
    }
    response = client.put('/customers/update_customer', json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Customer updated successfully"

def test_logout_customer(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.delete('/customers/logout_customer', headers=headers)
    assert response.status_code == 200
    assert response.json['message'] == "Customer logged out successfully"

def test_get_customer_info(client, customer_token):
    headers = {"Authorization": f"Bearer {customer_token}"}
    response = client.post('/customers/get_customer_info', headers=headers)
    assert response.status_code == 200
    assert "username" in response.json
    assert response.json["username"] == "customer"
