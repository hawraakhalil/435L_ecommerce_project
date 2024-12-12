from werkzeug.exceptions import NotFound, BadRequest
from shared.models.CustomersModel import Customer
from shared.models.TransactionsModel import Transaction


class CustomerManagementService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_customer(self, customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).first()
        if not customer:
            raise NotFound(f'Customer with id {customer_id} not found')
        return customer

    def top_up_customer(self, data):
        customer_id = data['customer_id']
        amount = data['amount']
        currency = data['currency']

        customer = self.get_customer(customer_id)
        
        if customer.status != 'active':
            raise BadRequest(f'Customer with id {customer_id} is {customer.status}')

        if currency == 'LBP':        
            customer.lbp_balance += amount
        else:
            customer.usd_balance += amount

        self.db_session.commit()
        return {'lbp_balance': customer.lbp_balance, 'usd_balance': customer.usd_balance}
    
    def update_customer_profile(self, data):
        customer_id = data['customer_id']
        first_name = data['first_name']
        last_name = data['last_name']
        phone = data['phone']
        age = data['age']
        gender = data['gender']
        marital_status = data['marital_status']

        customer = self.get_customer(customer_id)

        if first_name:
            customer.first_name = first_name
        if last_name:
            customer.last_name = last_name
        if phone:
            customer.phone = phone
        if age:
            customer.age = age
        if gender:
            customer.gender = gender
        if marital_status:
            customer.marital_status = marital_status

        self.db_session.commit()
        return customer.to_dict()

    def reverse_transaction(self, data):
        transaction_id = data['transaction_id']
        transaction = Transaction.query.filter(Transaction.id == transaction_id).first()
        if not transaction:
            raise NotFound(f'Transaction with id {transaction_id} not found')
        
        if transaction.status == 'reversed':
            raise BadRequest(f'Transaction with id {transaction_id} is already reversed')
        
        transaction.status = 'reversed'
        self.db_session.commit()
        return {'message': 'Transaction reversed successfully'}
    
    def get_customer_info(self, data):
        customer_id = data['customer_id']
        customer = self.get_customer(customer_id)
        return customer.to_dict()
    
    def get_customer_transactions(self, data):
        customer_id = data['customer_id']
        customer = self.get_customer(customer_id)
        return [transaction.to_dict() for transaction in customer.transactions]

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

    def get_all_customers(self, data):
        customers = Customer.query.all()
        return [customer.to_dict() for customer in customers]

    def get_all_banned_customers(self, data):
        customers = Customer.query.filter(Customer.status == 'banned').all()
        return [customer.to_dict() for customer in customers]
