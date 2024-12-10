from shared.models.ItemsModel import Item
from werkzeug.exceptions import NotFound

class InventoryService:
    def __init__(self, db_session):
        self.db_session = db_session
    
    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.filter_by(id=item_id).first()
    
    @staticmethod
    def get_item_by_name(name):
        return Item.query.filter_by(name=name).first()
    
    def get_item(self, item_id, name):
        item = self.get_item_by_id(item_id) or self.get_item_by_name(name)
        if not item:
            raise NotFound(f'Item with identifier {item_id or name} not found')
        return item

    def add_item(self, data):
        name = data.get('name')
        category = data.get('category')
        price_per_unit = data.get('price_per_unit')
        currency = data.get('currency')
        quantity = data.get('quantity')
        description = data.get('description')

        if self.get_item_by_name(name):
            raise ValueError(f'Item with name {name} already exists')

        item = Item(name=name, category=category, price_per_unit=price_per_unit, currency=currency, quantity=quantity, description=description)
        self.db_session.add(item)
        self.db_session.commit()
        return {'message': f'Item with id {item.id} added successfully'}
    
    def restock_item(self, data):
        item_id = data.get('item_id')
        name = data.get('name')
        quantity = data.get('quantity')

        item = self.get_item(item_id, name)

        item.quantity += quantity
        self.db_session.commit()
        return {'message': f'Item with id {item.id} restocked successfully'}
    
    def update_item(self, data):
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item(item_id, name)

        category = data.get('category')
        price_per_unit = data.get('price_per_unit')
        currency = data.get('currency')
        quantity = data.get('quantity')
        description = data.get('description')

        item.category = category if category else item.category
        item.price_per_unit = price_per_unit if price_per_unit else item.price_per_unit
        item.currency = currency if currency else item.currency
        item.quantity = quantity if quantity else item.quantity
        item.description = description if description else item.description

        self.db_session.commit()
        return {'message': f'Item with id {item.id} updated successfully'}

    @staticmethod
    def get_items():
        return {'items': [item.to_dict() for item in Item.query.all()]}

    def delete_item(self, data):
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item(item_id, name)
        self.db_session.delete(item)
        self.db_session.commit()
        return {'message': f'Item with id {item.id} deleted successfully'}
    
    def get_items_by_category(self, data):
        category = data.get('category')
        items = Item.query.filter_by(category=category).all()
        return {'items': [item.to_dict() for item in items]}


