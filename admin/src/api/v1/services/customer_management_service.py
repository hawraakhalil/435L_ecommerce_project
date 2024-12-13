from werkzeug.exceptions import NotFound, BadRequest
from admin.src.model.CustomersModel import Customer
from admin.src.model.TransactionsModel import Transaction

from admin.src.utils.logger import logger


class CustomerManagementService:
    def __init__(self, db_session):
        self.db_session = db_session

    @staticmethod
    def get_customer(customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFound(f'Customer with id {customer_id} not found')
        return customer

    @staticmethod
    def get_transaction(transaction_id):
        transaction = Transaction.query.filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise NotFound(f'Transaction with id {transaction_id} not found')
        return transaction
    
    @staticmethod
    def get_customer_transactions(customer_id):
        transaction = Transaction.query.filter(Transaction.customer_id == customer_id).first()
        if not transaction:
            raise NotFound(f'Customer with id {customer_id} has no transactions to show')
        return transaction

    def top_up_customer(self, data):
        logger.info('Enter top up customer service')
        customer_id = data['customer_id']
        amount = data['amount']
        currency = data['currency']
        logger.info(f'Top up customer service: customer_id: {customer_id}, amount: {amount}, currency: {currency}')

        customer = self.get_customer(customer_id)
        
        if customer.status != 'active':
            logger.info(f'Customer with id {customer_id} is {customer.status}')
            raise BadRequest(f'Customer with id {customer_id} is {customer.status}')

        if currency == 'LBP':  
            customer.lbp_balance += amount
        else:
            customer.usd_balance += amount

        self.db_session.commit()
        logger.info(f'Top up customer successfully')
        return {'lbp_balance': customer.lbp_balance, 'usd_balance': customer.usd_balance}
    
    def update_customer_profile(self, data):
        logger.info('Enter update customer profile service')

        # Ensure customer_id is always provided
        customer_id = data.get('customer_id')
        if not customer_id:
            logger.error('Customer ID is missing')
            raise ValueError('Customer ID is required')

        customer = self.get_customer(customer_id)

        # Dynamically update only the fields present in the data
        if 'first_name' in data:
            logger.info(f'Updating first_name to: {data["first_name"]}')
            customer.first_name = data['first_name']
        if 'last_name' in data:
            logger.info(f'Updating last_name to: {data["last_name"]}')
            customer.last_name = data['last_name']
        if 'phone' in data:
            logger.info(f'Updating phone to: {data["phone"]}')
            customer.phone = data['phone']
        if 'age' in data:
            logger.info(f'Updating age to: {data["age"]}')
            customer.age = data['age']
        if 'gender' in data:
            logger.info(f'Updating gender to: {data["gender"]}')
            customer.gender = data['gender']
        if 'marital_status' in data:
            logger.info(f'Updating marital_status to: {data["marital_status"]}')
            customer.marital_status = data['marital_status']

        # Commit the updates to the database
        self.db_session.commit()
        logger.info('Customer profile updated successfully')
        return customer.to_dict()

    def reverse_transaction(self, data):
        logger.info('Enter reverse transaction service')
        transaction_id = data['transaction_id']
        transaction = self.get_transaction(transaction_id)
        
        if transaction.status == 'reversed':
            logger.info(f'Transaction with id {transaction_id} is already reversed')
            raise BadRequest(f'Transaction with id {transaction_id} is already reversed')
        
        transaction.status = 'reversed'
        self.db_session.commit()
        logger.info(f'Transaction reversed successfully')
        return {'message': 'Transaction reversed successfully'}
    
    def get_customer_info(self, data):
        logger.info('Enter get customer info service')
        customer_id = data['customer_id']
        customer = self.get_customer(customer_id)
        logger.info(f'Get customer info service: customer_id: {customer_id}')
        return customer.to_dict()
    
    def get_customer_transactions(self, data):
        customer_id = data['customer_id']
        transactions = self.get_customer_transactions(customer_id)
        return [transaction.to_dict() for transaction in transactions]

    def ban_customer(self, data):
        customer_id = data['customer_id']
        customer = self.get_customer(customer_id)
        customer.status = 'banned'
        self.db_session.commit()
        return {'message': 'Customer banned successfully'}

    def unban_customer(self, data):
        customer_id = data['customer_id']
        customer = self.get_customer(customer_id)
        customer.status = 'active'
        self.db_session.commit()
        return {'message': 'Customer unbanned successfully'}

    def get_all_customers(self):
        customers = Customer.query.all()
        return [customer.to_dict() for customer in customers]

    def get_all_banned_customers(self):
        customers = Customer.query.filter(Customer.status == 'banned').all()
        return [customer.to_dict() for customer in customers]
