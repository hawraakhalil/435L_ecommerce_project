from datetime import datetime, timedelta
from sales.src.model.CustomersModel import Customer
from sales.src.model.ItemsModel import Item
from sales.src.model.TransactionsModel import Transaction
from werkzeug.exceptions import NotFound, BadRequest
from sales.src.utils.errors import InsufficientStock, InsufficientBalance
from sales.src.utils.logger import logger

class SalesService:
    def __init__(self, db_session):
        self.db_session = db_session

    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.filter(Item.id == item_id).first()
    
    @staticmethod
    def get_item_by_name(item_name):
        return Item.query.filter(Item.name == item_name).first()

    def get_item(self, item_id, item_name):
        item = self.get_item_by_id(item_id) or self.get_item_by_name(item_name)
        if not item:
            logger.info(f'Item with id {item_id} or name {item_name} not found')
            raise NotFound(f'Item with id {item_id} or name {item_name} not found')
        return item
    
    @staticmethod
    def get_customer(customer_username):
        customer = Customer.query.filter(Customer.username == customer_username).first()
        if not customer:
            logger.info(f'Customer with username {customer_username} not found')
            raise NotFound(f'Customer with username {customer_username} not found')
        return customer
    
    @staticmethod
    def get_transaction(transaction_id):
        transaction = Transaction.query.filter(Transaction.id == transaction_id).first()
        if not transaction:
            logger.info(f'Transaction with id {transaction_id} not found')
            raise NotFound(f'Transaction with id {transaction_id} not found')
        return transaction

    def purchase(self, data, customer_username):
        logger.info('Enter purchase')
        item_ids = data.get('item_ids', [])
        item_quantities = data.get('item_quantities', [])
        logger.info(f'Item ids: {item_ids}')
        logger.info(f'Item quantities: {item_quantities}')

        customer = self.get_customer(customer_username)

        items = []
        items_quantities = []
        total_lbp_price = 0
        total_usd_price = 0

        for index in range(len(item_ids)):
            item_id = item_ids[index]
            quantity = item_quantities[index]
            item = self.get_item(item_id)

            if item.quantity < quantity:
                logger.info(f'Item {item.id} with name {item.name} has only {item.quantity} left in stock')
                raise InsufficientStock(f'Item {item.id} with name {item.name} has only {item.quantity} left in stock')
            
            if item.currency == 'LBP':
                total_lbp_price += item.price_per_unit * quantity
            else: 
                total_usd_price += item.price_per_unit * quantity

            items.append(item)
            items_quantities.append(quantity)

        if customer.lbp_balance < total_lbp_price:
            logger.info(f'Customer {customer.id} has insufficient LBP balance. Required: {total_lbp_price}, Available: {customer.lbp_balance}')
            raise InsufficientBalance(
                f'Customer {customer.id} has insufficient LBP balance. '
                f'Required: {total_lbp_price}, Available: {customer.lbp_balance}'
            )

        if customer.usd_balance < total_usd_price:
            logger.info(f'Customer {customer.id} has insufficient USD balance. Required: {total_usd_price}, Available: {customer.usd_balance}')
            raise InsufficientBalance(
                f'Customer {customer.id} has insufficient USD balance. '
                f'Required: {total_usd_price}, Available: {customer.usd_balance}'
            )

        customer.lbp_balance -= total_lbp_price
        customer.usd_balance -= total_usd_price

        for item, quantity in zip(items, items_quantities):
            item.quantity -= quantity

        transaction = Transaction(
            customer_id=customer.id,
            items=[item.to_dict() for item in items],
            items_quantities=items_quantities,
            lbp_total_price=total_lbp_price,
            usd_total_price=total_usd_price,
        )

        self.db_session.add(transaction)
        self.db_session.commit()
        logger.info('Transaction added successfully')
        return transaction.to_dict()

    def reverse_purchase(self, data, customer_username):
        logger.info('Enter reverse purchase')
        transaction_id = data.get('transaction_id')
        transaction = self.get_transaction(transaction_id)
        customer = self.get_customer(customer_username)

        if transaction.customer_id != customer.id:
            logger.info(f'Transaction with id {transaction_id} does not belong to customer with username {customer_username}')
            raise BadRequest(f'Transaction with id {transaction_id} does not belong to customer with username {customer_username}')
        
        if transaction.status != 'completed':
            logger.info(f'Transaction with id {transaction_id} is already reversed')
            raise BadRequest(f'Transaction with id {transaction_id} is already reversed')
        
        if transaction.created_at < datetime.now() - timedelta(days=10):
            logger.info(f'Transaction with id {transaction_id} is older than 10 days and cannot be reversed')
            raise BadRequest(f'Transaction with id {transaction_id} is older than 10 days and cannot be reversed')

        customer.lbp_balance += transaction.lbp_total_price
        customer.usd_balance += transaction.usd_total_price

        for item, quantity in zip(transaction.items, transaction.items_quantities):
            item.quantity += quantity

        transaction.status = 'reversed'
        self.db_session.commit()
        logger.info('Transaction reversed successfully')
        return transaction.to_dict()

    def get_customer_transactions(self, customer_username):
        logger.info('Enter get customer transactions')
        customer = self.get_customer(customer_username)
        transactions = Transaction.query.filter(Transaction.customer_id == customer.id).all()
        logger.info(f'Transactions retrieved successfully')
        return [transaction.to_dict() for transaction in transactions]

    def inquire_item(self, data):
        logger.info('Enter inquire item')
        item_id = data.get('item_id')
        name = data.get('name')
        item = self.get_item(item_id, name)
        logger.info(f'Item retrieved successfully')
        return item.to_dict()

    def get_all_items(self):
        logger.info('Enter get all items')
        items = Item.query.all()
        logger.info(f'Items retrieved successfully')
        return [item.to_dict() for item in items]
