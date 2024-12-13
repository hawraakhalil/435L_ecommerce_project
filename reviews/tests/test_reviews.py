import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from reviews.app import create_app
from reviews.src.extensions import db
from reviews.src.model.CustomersModel import Customer
from reviews.src.model.ItemsModel import Item
from reviews.src.model.ReviewsModel import Review


@pytest.fixture
def app():
    """Create and configure a new app instance for testing."""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for testing
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        seed_database()  # Seed the database with mock data
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()


def seed_database():
    """Seed the database with mock data for testing."""
    customer = Customer(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
        first_name="Test",
        last_name="User",
        phone="123456789",
        age=25,
        gender="male",
        marital_status="single",
        lbp_balance=100000,
        usd_balance=1000,
        items=[],
    )
    customer.set_password("testpassword")

    item1 = Item(
        id=1,
        name="Laptop",
        category="Electronics",
        price_per_unit=500,
        currency="USD",
        quantity=10,
        description="A high-end laptop",
    )
    item2 = Item(
        id=2,
        name="Phone",
        category="Electronics",
        price_per_unit=300,
        currency="USD",
        quantity=5,
        description="A smartphone",
    )

    db.session.add(customer)
    db.session.add(item1)
    db.session.add(item2)
    db.session.commit()


def get_test_token():
    """Generate a valid JWT token for testing."""
    return create_access_token(identity="testuser")


def test_add_review(client):
    """Test the add_review endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    data = {
        "item_id": 1,
        "rating": 5,
        "comment": "Excellent product!",
    }
    response = client.put("/reviews/add_review", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json["rating"] == 5
    assert response.json["comment"] == "Excellent product!"


def test_update_review(client):
    """Test the update_review endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    # First, add a review
    client.put(
        "/reviews/add_review",
        json={"item_id": 1, "rating": 5, "comment": "Good product"},
        headers=headers,
    )
    # Update the review
    data = {
        "item_id": 1,
        "rating": 4,
        "comment": "Updated review: Great product!",
    }
    response = client.put("/reviews/update_review", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json["rating"] == 4
    assert response.json["comment"] == "Updated review: Great product!"


def test_delete_review(client):
    """Test the delete_review endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    # First, add a review
    client.put(
        "/reviews/add_review",
        json={"item_id": 1, "rating": 5, "comment": "Nice product"},
        headers=headers,
    )
    # Delete the review
    data = {"item_id": 1}
    response = client.delete("/reviews/delete_review", json=data, headers=headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json["message"]


def test_get_customer_reviews(client):
    """Test the get_customer_reviews endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    # Add a review
    client.put(
        "/reviews/add_review",
        json={"item_id": 1, "rating": 5, "comment": "Great product!"},
        headers=headers,
    )
    # Fetch customer reviews
    data = {"customer_username": "testuser"}
    response = client.post("/reviews/get_customer_reviews", json=data, headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["rating"] == 5
    assert response.json[0]["comment"] == "Great product!"


def test_get_item_reviews(client):
    """Test the get_item_reviews endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    # Add a review
    client.put(
        "/reviews/add_review",
        json={"item_id": 1, "rating": 4, "comment": "Nice item"},
        headers=headers,
    )
    # Fetch item reviews
    data = {"item_id": 1}
    response = client.post("/reviews/get_item_reviews", json=data, headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["rating"] == 4
    assert response.json[0]["comment"] == "Nice item"


def test_get_all_reviews(client):
    """Test the get_all_reviews endpoint."""
    headers = {"Authorization": f"Bearer {get_test_token()}"}
    # Add reviews
    client.put(
        "/reviews/add_review",
        json={"item_id": 1, "rating": 5, "comment": "Great product!"},
        headers=headers,
    )
    client.put(
        "/reviews/add_review",
        json={"item_id": 2, "rating": 3, "comment": "Average product"},
        headers=headers,
    )
    # Fetch all reviews
    response = client.get("/reviews/get_all_reviews", headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2
