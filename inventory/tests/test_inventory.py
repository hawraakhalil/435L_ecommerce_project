import pytest
from flask import Flask
from inventory.app import create_app
from inventory.src.extensions import db
from inventory.src.model.ItemsModel import Item
from flask_jwt_extended import create_access_token
from datetime import timedelta

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def setup_database(client):
    """Set up initial test data for the database."""
    item1 = Item(
        name="Laptop",
        category="electronics",
        price_per_unit=1000,
        currency="USD",
        quantity=10,
        description="A powerful laptop",
    )
    item2 = Item(
        name="Chair",
        category="furniture",
        price_per_unit=50,
        currency="USD",
        quantity=100,
        description="A comfortable chair",
    )
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()

def get_test_token():
    """Generate a valid JWT token for tests."""
    # Replace 'testuser' with the identity used in your application (e.g., an admin username).
    test_identity = "testuser"
    # Create the token using the same expiration settings as in your app.
    return create_access_token(identity=test_identity, expires_delta=timedelta(hours=1))


def test_add_item(client):
    """Test adding a new item."""
    data = {
        "name": "Table",
        "category": "furniture",
        "price_per_unit": 200,
        "currency": "USD",
        "quantity": 50,
        "description": "A wooden table",
    }
    response = client.post("/inventory/add_item", json=data)
    assert response.status_code == 200
    assert "Item with id" in response.json["message"]


def test_restock_item(client, setup_database):
    """Test restocking an existing item."""
    data = {"name": "Laptop", "quantity": 5}
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.post("/inventory/restock_item", json=data, headers=headers)
    assert response.status_code == 200
    assert "restocked successfully" in response.json["message"]


def test_update_item(client, setup_database):
    """Test updating an existing item."""
    data = {
        "name": "Laptop",
        "price_per_unit": 1200,
        "description": "An updated description",
    }
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.put("/inventory/update_item", json=data, headers=headers)
    assert response.status_code == 200
    assert "updated successfully" in response.json["message"]


def test_delete_item(client, setup_database):
    """Test deleting an existing item."""
    data = {"name": "Chair"}
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.delete("/inventory/delete_item", json=data, headers=headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json["message"]


def test_get_item(client, setup_database):
    """Test fetching an item by name."""
    data = {"name": "Laptop"}
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.post("/inventory/get_item", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json["name"] == "Laptop"


def test_get_items(client, setup_database):
    """Test fetching all items."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.get("/inventory/get_items", headers=headers)
    assert response.status_code == 200
    assert len(response.json["items"]) == 2


def test_get_items_by_category(client, setup_database):
    """Test fetching items by category."""
    data = {"category": "furniture"}
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    response = client.post("/inventory/get_items_by_category", json=data, headers=headers)
    assert response.status_code == 200
    assert len(response.json["items"]) == 1
    assert response.json["items"][0]["name"] == "Chair"
