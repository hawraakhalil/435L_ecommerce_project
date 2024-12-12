from datetime import datetime, timedelta
from shared.db import db
from shared.models.TransactionsModel import Transaction
from shared.models.ItemsModel import Item
from shared.models.CustomersModel import Customer
from werkzeug.exceptions import NotFound, BadRequest
from sales.src.errors import InsufficientStock, InsufficientBalance


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
    
    def get_transaction(self, transaction_id):
        transaction = Transaction.query.filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise NotFound(f'Transaction with id {transaction_id} not found')
        return transaction

    def purchase(self, data, customer_id):
        item_ids_or_names = data.get('item_ids_or_names', [])
        item_quantities = data.get('item_quantities', [])

        customer = self.get_customer_by_id(customer_id)

        items = []
        items_quantities = []
        total_lbp_price = 0
        total_usd_price = 0

        for index in range(len(item_ids_or_names)):
            item_id_or_name = item_ids_or_names[index]
            quantity = item_quantities[index]
            if item_id_or_name.isdigit():
                item = self.get_item_by_id(int(item_id_or_name))
            else:
                item = self.get_item_by_name(item_id_or_name)
            
            if item.quantity < quantity:
                raise InsufficientStock(f'Item {item.id} with name {item.name} has only {item.quantity} left in stock')
            
            if item.currency == 'LBP':
                total_lbp_price += item.price_per_unit * quantity
            else: 
                total_usd_price += item.price_per_unit * quantity

            items.append(item)
            items_quantities.append(quantity)

        if customer.lbp_balance < total_lbp_price:
            raise InsufficientBalance(
                f'Customer {customer.id} has insufficient LBP balance. '
                f'Required: {total_lbp_price}, Available: {customer.lbp_balance}'
            )

        if customer.usd_balance < total_usd_price:
            raise InsufficientBalance(
                f'Customer {customer.id} has insufficient USD balance. '
                f'Required: {total_usd_price}, Available: {customer.usd_balance}'
            )

        customer.lbp_balance -= total_lbp_price
        customer.usd_balance -= total_usd_price

        for item, quantity in zip(items, items_quantities):
            item.quantity -= quantity

        transaction = Transaction(
            items_quantities=items_quantities,
            lbp_total_price=total_lbp_price,
            usd_total_price=total_usd_price,
            items=items,
            customer=customer,
        )
        
        self.db_session.add(transaction)
        self.db_session.commit()
        return transaction.to_dict()

    def reverse_purchase(self, data, customer_id):
        transaction_id = data.get('transaction_id')
        transaction = self.get_transaction(transaction_id)
        customer = self.get_customer_by_id(customer_id)

        if transaction.customer.id != customer.id:
            raise BadRequest(f'Transaction with id {transaction_id} does not belong to customer with id {customer_id}')
        
        if transaction.status != 'completed':
            raise BadRequest(f'Transaction with id {transaction_id} is already reversed')
        
        if transaction.created_at < datetime.now() - timedelta(days=10):
            raise BadRequest(f'Transaction with id {transaction_id} is older than 10 days and cannot be reversed')

        customer.lbp_balance += transaction.lbp_total_price
        customer.usd_balance += transaction.usd_total_price

        for item, quantity in zip(transaction.items, transaction.items_quantities):
            item.quantity += quantity

        transaction.status = 'reversed'
        self.db_session.commit()
        return transaction.to_dict()

    def get_user_transactions(self, user_id):
        transactions = Transaction.query.filter(Transaction.customer_id == user_id).all()
        return [transaction.to_dict() for transaction in transactions]

    def inquire_item(self, data):
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item_by_id(item_id) if item_id else self.get_item_by_name(name)
        return item.to_dict()

    def get_all_items(self):
        items = Item.query.all()
        return [item.to_dict() for item in items]
