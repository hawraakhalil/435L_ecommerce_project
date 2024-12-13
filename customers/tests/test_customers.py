import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from customers.src.extensions import db
from customers.app import create_app
from customers.src.model.CustomersModel import Customer

@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory database
    app.config["JWT_SECRET_KEY"] = "test_secret_key"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def setup_database(app):
    """Populate the database with a test customer."""
    with app.app_context():
        # Add a sample customer
        customer = Customer(
            username="testuser",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            phone="71000000",
            age=25,
            gender="male",
            marital_status="single",
        )
        customer.set_password("password123")  # Set hashed password
        db.session.add(customer)
        db.session.commit()


@pytest.fixture
def auth_headers(app, setup_database):
    """Generate authentication headers for a test customer."""
    with app.app_context():
        # Generate a valid JWT token for the test user
        access_token = create_access_token(identity="testuser")
        return {"Authorization": f"Bearer {access_token}"}
    
def test_register_customer(client):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "password123",
        "first_name": "New",
        "last_name": "User",
        "phone": "72000000",
        "age": 30,
        "gender": "female",
        "marital_status": "single",
    }
    response = client.put("/customers/register_customer", json=data)
    assert response.status_code == 201
    assert "access" in response.json
    assert "refresh" in response.json


def test_register_customer_validation_error(client):
    data = {"username": "newuser"}
    response = client.put("/customers/register_customer", json=data)
    assert response.status_code == 400
    assert "Validation error" in response.json["error"]


def test_login_customer(client, setup_database):
    """Test customer login."""
    data = {"identifier": "testuser", "password": "password123"}
    response = client.post("/customers/login_customer", json=data)
    assert response.status_code == 200
    assert "access" in response.json
    assert "refresh" in response.json


def test_login_customer_invalid_credentials(client, setup_database):
    """Test login with invalid credentials."""
    data = {"identifier": "testuser", "password": "wrongpassword"}
    response = client.post("/customers/login_customer", json=data)
    assert response.status_code == 403
    assert "Invalid password for customer with username or email: testuser" in response.json["error"]


def test_logout_customer(client, auth_headers):
    response = client.delete("/customers/logout_customer", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["message"] == "Customer logged out successfully"


def test_update_customer(client, auth_headers):
    data = {"first_name": "UpdatedName"}
    response = client.put("/customers/update_customer", json=data, headers=auth_headers)
    assert response.status_code == 200
    assert response.json["message"] == "Customer updated successfully"


def test_update_customer_validation_error(client, auth_headers):
    data = {}
    response = client.put("/customers/update_customer", json=data, headers=auth_headers)
    assert response.status_code == 400
    assert "Validation error" in response.json["error"]


def test_get_customer_info(client, auth_headers):
    response = client.post("/customers/get_customer_info", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["username"] == "testuser"
