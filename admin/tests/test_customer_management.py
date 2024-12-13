import pytest
from flask_jwt_extended import create_access_token
from admin.app import create_app
from admin.src.extensions import db
from admin.src.model.CustomersModel import Customer


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(app):
    with app.app_context():
        customer = Customer(
            username='testcustomer',
            email='testcustomer@example.com',
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

        access_token = create_access_token(identity='testcustomer')
        return {'Authorization': f'Bearer {access_token}'}


def test_top_up_customer(client, auth_headers):
    data = {
        "customer_id": 1,
        "amount": 100.0,
        "currency": "USD"
    }
    response = client.put('/admin/customers/top_up_customer', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert 'usd_balance' in response.json


def test_update_customer_profile(client, auth_headers):
    data = {
        "customer_id": 1,
        "first_name": "UpdatedName"
    }
    response = client.put('/admin/customers/update_customer_profile', json=data, headers=auth_headers)
    assert response.status_code == 200


def test_get_customer_info(client, auth_headers):
    data = {
        "customer_id": 1
    }
    response = client.get('/admin/customers/get_customer_info', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['username'] == 'testcustomer'


def test_ban_customer(client, auth_headers):
    data = {
        "customer_id": 1
    }
    response = client.put('/admin/customers/ban_customer', json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json['message'] == 'Customer banned successfully'
