from werkzeug.exceptions import NotFound, BadRequest

from inventory.src.model.ItemsModel import Item
from inventory.src.utils.logger import logger


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
            logger.info(f'Item with identifier {item_id or name} not found')
            raise NotFound(f'Item with identifier {item_id or name} not found')
        return item

    def add_item(self, data):
        logger.info('Enter add item')
        name = data.get('name')
        category = data.get('category')
        price_per_unit = data.get('price_per_unit')
        currency = data.get('currency')
        quantity = data.get('quantity')
        description = data.get('description')

        if self.get_item_by_name(name):
            logger.info(f'Item with name {name} already exists')
            raise BadRequest(f'Item with name {name} already exists')

        item = Item(name=name, category=category, price_per_unit=price_per_unit, currency=currency, quantity=quantity, description=description)
        self.db_session.add(item)
        self.db_session.commit()
        logger.info('Item added successfully')
        return {'message': f'Item with id {item.id} added successfully'}
    
    def restock_item(self, data):
        logger.info('Enter restock item')
        item_id = data.get('item_id')
        name = data.get('name')
        quantity = data.get('quantity')

        item = self.get_item(item_id, name)

        item.quantity += quantity
        self.db_session.commit()
        logger.info('Item restocked successfully')
        return {'message': f'Item with id {item.id} restocked successfully'}
    
    def update_item(self, data):
        logger.info('Enter update item')
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item(item_id, name)

        category = data.get('category')
        price_per_unit = data.get('price_per_unit')
        currency = data.get('currency')
        quantity = data.get('quantity')
        description = data.get('description')

        if category:
            logger.info(f'Updating category for item with id {item.id} to {category}')
            item.category = category
        if price_per_unit:
            logger.info(f'Updating price per unit for item with id {item.id} to {price_per_unit}')
            item.price_per_unit = price_per_unit
        if currency:
            logger.info(f'Updating currency for item with id {item.id} to {currency}')
            item.currency = currency
        if quantity:
            logger.info(f'Updating quantity for item with id {item.id} to {quantity}')
            item.quantity = quantity
        if description:
            logger.info(f'Updating description for item with id {item.id} to {description}')
            item.description = description

        self.db_session.commit()
        logger.info('Item updated successfully')
        return {'message': f'Item with id {item.id} updated successfully'}

    def delete_item(self, data):
        logger.info('Enter delete item service')
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item(item_id, name)
        self.db_session.delete(item)
        self.db_session.commit()
        logger.info('Item deleted successfully')
        return {'message': f'Item with id {item.id} deleted successfully'}
    
    @staticmethod
    def get_items():
        logger.info('Enter get items service')
        return {'items': [item.to_dict() for item in Item.query.all()]}

    def get_items_by_category(self, data):
        logger.info('Enter get items by category service')
        category = data.get('category')
        items = Item.query.filter_by(category=category).all()
        logger.info('Items fetched successfully')
        return {'items': [item.to_dict() for item in items]}
