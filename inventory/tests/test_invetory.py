import pytest
from flask import Flask
from shared.db import db
from inventory.src.api.v1.inventory_service import InventoryService
from inventory.src.api.v1.inventory_schema import (
    AddItemSchema, RestockItemSchema, UpdateItemSchema, ItemSchema, CategorySchema
)
from shared.models.ItemsModel import Item

# Setup test database and app
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
def inventory_service(db_session):
    return InventoryService(db_session=db_session)

# Test InventoryService methods
def test_add_item(inventory_service, db_session):
    data = {
        'name': 'Test Item',
        'category': 'electronics',
        'price_per_unit': 100,
        'currency': 'USD',
        'quantity': 10,
        'description': 'A test item description.'
    }
    result = inventory_service.add_item(data)
    assert 'Item with id' in result['message']
    assert db_session.query(Item).filter_by(name='Test Item').first() is not None

def test_restock_item(inventory_service, db_session):
    item = Item(
        name='Test Item',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='A test item description.'
    )
    db_session.add(item)
    db_session.commit()

    data = {'item_id': item.id, 'quantity': 5}
    result = inventory_service.restock_item(data)
    assert 'restocked successfully' in result['message']
    assert item.quantity == 15

def test_update_item(inventory_service, db_session):
    item = Item(
        name='Test Item',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='A test item description.'
    )
    db_session.add(item)
    db_session.commit()

    data = {'item_id': item.id, 'price_per_unit': 150, 'description': 'Updated description.'}
    result = inventory_service.update_item(data)
    assert 'updated successfully' in result['message']
    assert item.price_per_unit == 150
    assert item.description == 'Updated description.'

def test_delete_item(inventory_service, db_session):
    item = Item(
        name='Test Item',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='A test item description.'
    )
    db_session.add(item)
    db_session.commit()

    data = {'item_id': item.id}
    result = inventory_service.delete_item(data)
    assert 'deleted successfully' in result['message']
    assert db_session.query(Item).filter_by(id=item.id).first() is None

def test_get_item(inventory_service, db_session):
    item = Item(
        name='Test Item',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='A test item description.'
    )
    db_session.add(item)
    db_session.commit()

    result = inventory_service.get_item(item_id=item.id, name=None)
    assert result.name == 'Test Item'

    result = inventory_service.get_item(item_id=None, name='Test Item')
    assert result.name == 'Test Item'

def test_get_items(inventory_service, db_session):
    item1 = Item(
        name='Test Item 1',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='First test item.'
    )
    item2 = Item(
        name='Test Item 2',
        category='furniture',
        price_per_unit=200,
        currency='USD',
        quantity=5,
        description='Second test item.'
    )
    db_session.add(item1)
    db_session.add(item2)
    db_session.commit()

    result = inventory_service.get_items()
    assert len(result['items']) == 2

def test_get_items_by_category(inventory_service, db_session):
    item1 = Item(
        name='Test Item 1',
        category='electronics',
        price_per_unit=100,
        currency='USD',
        quantity=10,
        description='First test item.'
    )
    item2 = Item(
        name='Test Item 2',
        category='furniture',
        price_per_unit=200,
        currency='USD',
        quantity=5,
        description='Second test item.'
    )
    db_session.add(item1)
    db_session.add(item2)
    db_session.commit()

    data = {'category': 'electronics'}
    result = inventory_service.get_items_by_category(data)
    assert len(result['items']) == 1
    assert result['items'][0]['name'] == 'Test Item 1'
