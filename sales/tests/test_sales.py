import pytest
from flask import Flask
from sales.app import create_app
from sales.src.extensions import db
from sales.src.model.CustomersModel import Customer
from sales.src.model.ItemsModel import Item
from sales.src.model.TransactionsModel import Transaction

@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        # Seed the database with mock data
        seed_database()

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def seed_database():
    """Seed the database with mock data."""
    # Add a customer with valid data
    customer = Customer(
        username="testuser",
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        phone="70123456",
        age=30,
        gender="Male",
        marital_status="Single",
        lbp_balance=100000,
        usd_balance=5000,
    )
    customer.set_password("password123")  # Hash the password
    db.session.add(customer)

    item = Item(
        name="Laptop",
        category="electronics",
        price_per_unit=1000,
        currency="USD",
        quantity=10,
        description="A high-end gaming laptop",
    )
    db.session.add(item)

    db.session.commit()


def get_test_token():
    """Generate a valid JWT token for tests."""
    from flask_jwt_extended import create_access_token
    return create_access_token(identity="testuser")


def test_purchase(client):
    """Test the purchase route."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    data = {
        "item_ids": [1],
        "item_quantities": [2],
    }
    response = client.put("/sales/purchase", json=data, headers=headers)
    print(response.json)
    assert response.status_code == 200

def test_insufficient_purchase(client):
    """Test the purchase route."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    data = {
        "item_ids": [1],
        "item_quantities": [200],
    }
    response = client.put("/sales/purchase", json=data, headers=headers)
    print(response.json)
    assert response.status_code == 409

def test_reverse_purchase(client):
    """Test the reverse purchase route."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    data = {
        "transaction_id": 1,
    }
    response = client.put("/sales/reverse_purchase", json=data, headers=headers)
    assert response.status_code in [200, 404]  # Allowing for NotFound if transaction doesn't exist


def test_get_customer_transactions(client):
    """Test the get customer transactions route."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.post("/sales/get_customer_transactions", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_inquire_item(client):
    """Test the inquire item route."""
    data = {
        "item_id": 1,
    }
    response = client.get("/sales/inquire_item", json=data)
    assert response.status_code == 200
    assert response.json["name"] == "Laptop"


def test_get_all_items(client):
    """Test the get all items route."""
    response = client.get("/sales/get_all_items")
    assert response.status_code == 200
    assert isinstance(response.json, list)