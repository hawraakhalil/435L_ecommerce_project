import pytest
from flask import Flask
from shared.db import db
from sales.src.api.v1.sales_service import SalesService
from shared.models.CustomersModel import Customer
from shared.models.ItemsModel import Item
from shared.models.TransactionsModel import Transaction
from sales.src.errors import InsufficientStock, InsufficientBalance

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
def db_session(app):
    with app.app_context():
        yield db.session

@pytest.fixture
def sales_service(db_session):
    return SalesService(db_session=db_session)

def create_customer_and_items(db_session):
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
        balance=1000
    )
    
    item1 = Item(
        name="Item 1",
        category="electronics",
        price_per_unit=100.0,
        currency="USD",
        quantity=10,
        description="Test item 1."
    )

    item2 = Item(
        name="Item 2",
        category="books",
        price_per_unit=50.0,
        currency="USD",
        quantity=5,
        description="Test item 2."
    )

    db_session.add(customer)
    db_session.add_all([item1, item2])
    db_session.commit()

    return customer, [item1, item2]

def test_purchase(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    data = {
        'item_ids_or_names': [str(items[0].id), str(items[1].id)],
        'item_quantities': [2, 3]
    }

    result = sales_service.purchase(data, customer.id)

    assert result['status'] == 'completed'
    assert result['total_price'] == 350.0
    assert items[0].quantity == 8
    assert items[1].quantity == 2
    assert customer.balance == 650.0

def test_purchase_insufficient_stock(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    data = {
        'item_ids_or_names': [str(items[0].id)],
        'item_quantities': [15]
    }

    with pytest.raises(InsufficientStock):
        sales_service.purchase(data, customer.id)

def test_purchase_insufficient_balance(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    data = {
        'item_ids_or_names': [str(items[0].id), str(items[1].id)],
        'item_quantities': [5, 5]
    }

    with pytest.raises(InsufficientBalance):
        sales_service.purchase(data, customer.id)

def test_reverse_purchase(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    transaction = Transaction(
        customer=customer,
        items=[items[0], items[1]],  # Ensure 'items' is a valid relationship
        total_price=200.0,
        status='completed'
    )
    db_session.add(transaction)
    db_session.commit()

    data = {'transaction_id': transaction.id}

    result = sales_service.reverse_purchase(data, customer.id)

    assert result['status'] == 'reversed'
    assert customer.balance == 1200.0
    assert items[0].quantity == 10

def test_reverse_purchase_invalid_customer(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    another_customer = Customer(
        username="anotheruser",
        email="anotheruser@example.com",
        password="password",
        first_name="Another",
        last_name="User",
        phone="9876543210",
        age=35,
        gender="Other",
        marital_status="Married",
        balance=500
    )
    transaction = Transaction(
        customer=customer,
        items=[items[0]],
        items_quantities=[2],
        total_price=200.0,
        status="completed"
    )
    db_session.add(another_customer)
    db_session.add(transaction)
    db_session.commit()

    data = {'transaction_id': transaction.id}

    with pytest.raises(BadRequest):
        sales_service.reverse_purchase(data, another_customer.id)

def test_get_user_transactions(sales_service, db_session):
    customer, items = create_customer_and_items(db_session)
    transaction1 = Transaction(
        customer=customer,
        items=[items[0]],
        items_quantities=[2],
        total_price=200.0,
        status="completed"
    )
    transaction2 = Transaction(
        customer=customer,
        items=[items[1]],
        items_quantities=[1],
        total_price=50.0,
        status="completed"
    )
    db_session.add_all([transaction1, transaction2])
    db_session.commit()

    result = sales_service.get_user_transactions(customer.id)

    assert len(result) == 2
    assert result[0]['total_price'] == 200.0
    assert result[1]['total_price'] == 50.0

def test_inquire_item(sales_service, db_session):
    _, items = create_customer_and_items(db_session)
    data = {'item_id': items[0].id}

    result = sales_service.inquire_item(data)

    assert result['name'] == "Item 1"
    assert result['quantity'] == 10

def test_get_all_items(sales_service, db_session):
    _, items = create_customer_and_items(db_session)

    result = sales_service.get_all_items()

    assert len(result) == 2
    assert result[0]['name'] == "Item 1"
    assert result[1]['name'] == "Item 2"
