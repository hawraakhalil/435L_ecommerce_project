import pytest
from flask import Flask
from shared.db import db
from reviews.src.api.v1.reviews_service import ReviewsService
from shared.models.CustomersModel import Customer
from shared.models.ItemsModel import Item
from shared.models.ReviewsModel import Review

@pytest.fixture
def app():
    app = Flask(_name_)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

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
def db_session(app):
    with app.app_context():
        yield db.session

@pytest.fixture
def reviews_service(db_session):
    return ReviewsService(db_session=db_session)

def create_customer_and_item(db_session):
    customer = Customer(
        username="testuser",
        email="testuser@example.com",
        password="password",
        first_name="Test",
        last_name="User",
        phone="1234567890",
        age=30,
        gender="Other",
        marital_status="Single",
        balance=100
    )
    item = Item(
        name="Test Item",
        category="electronics",
        price_per_unit=100.0,
        currency="USD",
        quantity=1,
        description="A test item."
    )
    db_session.add(customer)
    db_session.add(item)
    db_session.commit()
    return customer, item

def test_add_review(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    db_session.commit()

    data = {
        'item_id': item.id,
        'rating': 4.5,
        'comment': 'Great product!'
    }
    result = reviews_service.add_review(data, customer.id)

    assert result['item']['name'] == item.name
    assert result['rating'] == 4.5
    assert result['comment'] == 'Great product!'

def test_update_review(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    review = Review(customer=customer, item=item, rating=4.0, comment="Good item.")
    db_session.add(review)
    db_session.commit()

    data = {
        'item_id': item.id,
        'rating': 5.0,
        'comment': 'Excellent product!'
    }
    result = reviews_service.update_review(data, customer.id)

    assert result['rating'] == 5.0
    assert result['comment'] == 'Excellent product!'

def test_delete_review(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    review = Review(customer=customer, item=item, rating=4.0, comment="Good item.")
    db_session.add(review)
    db_session.commit()

    data = {'item_id': item.id}
    result = reviews_service.delete_review(data, customer.id)

    assert 'deleted successfully' in result['message']
    assert db_session.query(Review).filter_by(id=review.id).first() is None

def test_get_customer_reviews(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    review = Review(customer=customer, item=item, rating=4.0, comment="Good item.")
    db_session.add(review)
    db_session.commit()

    data = {'customer_username': customer.username}
    result = reviews_service.get_customer_reviews(data)

    assert len(result) == 1
    assert result[0]['comment'] == "Good item."

def test_get_item_reviews(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    review = Review(customer=customer, item=item, rating=4.0, comment="Good item.")
    db_session.add(review)
    db_session.commit()

    data = {'item_id': item.id}
    result = reviews_service.get_item_reviews(data)

    assert len(result) == 1
    assert result[0]['comment'] == "Good item."

def test_get_all_reviews(reviews_service, db_session):
    customer, item = create_customer_and_item(db_session)
    customer.items.append(item)
    review1 = Review(customer=customer, item=item, rating=4.0, comment="Good item.")
    review2 = Review(customer=customer, item=item, rating=5.0, comment="Excellent item.")
    db_session.add_all([review1, review2])
    db_session.commit()

    result = reviews_service.get_all_reviews()

    assert len(result) == 2
    assert any(review['comment'] == "Good item." for review in result)
    assert any(review['comment'] == "Excellent item." for review in result)
