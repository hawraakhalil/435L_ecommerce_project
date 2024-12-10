import requests
from shared.db import db
from shared.models.TransactionsModel import Transaction
from shared.models.ItemsModel import Item
from shared.models.CustomersModel import Customer
from werkzeug.exceptions import NotFound
import pybreaker
from sales.errors import InsufficientStock, InsufficientBalance


class SalesService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_item_by_id(self, item_id):
        item = Item.query.filter(Item.id == item_id).first()
        if not item:
            raise NotFound(f'Item with id {item_id} not found')
        return item

    def get_item_by_name(self, item_name):
        item = Item.query.filter(Item.name == item_name).first()
        if not item:
            raise NotFound(f'Item with name {item_name} not found')
        return item
    
    def get_customer_by_id(self, customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFound(f'Customer with id {customer_id} not found')
        return customer

    def purchase(self, data, customer_id):
        item_ids_or_names = data.get('item_ids_or_names', [])
        item_quantities = data.get('item_quantities', [])

        customer = self.get_customer_by_id(customer_id)

        items = []
        item_quantities = []
        total_price = 0

        for index in range(len(item_ids_or_names)):
            item_id_or_name = item_ids_or_names[index]
            quantity = item_quantities[index]
            if item_id_or_name.isdigit():
                item = self.get_item_by_id(int(item_id_or_name))
            else:
                item = self.get_item_by_name(item_id_or_name)
            
            if item.quantity < quantity:
                raise InsufficientStock(f'Item {item.id} with name {item.name} has only {item.quantity} left in stock')
            
            total_price += item.price_per_unit

            items.append(item)
            item_quantities.append(quantity)

        if customer.balance < total_price:
            raise InsufficientBalance(f'Customer {customer.id} has only {customer.balance} in balance')

        customer.balance -= total_price

        for item, quantity in zip(items, item_quantities):
            item.quantity -= quantity

        transaction = Transaction(items=items, item_quantities=item_quantities, total_price=total_price, status='completed')
        self.db_session.add(transaction)
        self.db_session.commit()
        return transaction.to_dict()

    def reverse_purchase(self, data):
        pass

    def get_transactions(self):
        pass


