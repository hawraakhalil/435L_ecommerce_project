from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.exceptions import NotFound, BadRequest
from customers.src.utils.utils import get_utc_now, format_phone
from customers.src.model.CustomersModel import Customer
from customers.src.utils.errors import AuthenticationError
from customers.src.utils.logger import logger

class CustomerService:
    def __init__(self, db_session):
        self.db_session = db_session

    @staticmethod
    def get_customer_by_username(username):
        return Customer.query.filter(Customer.username == username).first()

    @staticmethod
    def get_customer_by_email(email):
        return Customer.query.filter(Customer.email == email).first()
    
    @staticmethod
    def get_customer_by_phone(phone):
        return Customer.query.filter(Customer.phone == phone).first()
    
    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.query.filter(Customer.id == customer_id).first()

    def get_customer(self, identifier):
        customer = self.get_customer_by_username(identifier) or self.get_customer_by_email(identifier) or self.get_customer_by_phone(identifier) or self.get_customer_by_id(identifier)
        if not customer:
            logger.info(f'Customer with identifier {identifier} not found')
            raise NotFound(f'Customer with identifier {identifier} not found')
        return customer
    
    def register_customer(self, data):
        logger.info('Enter register customer service')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')
        gender = data.get('gender')
        marital_status = data.get('marital_status')

        logger.info(f'Register customer service: {first_name}, {last_name}, {username}, {password}, {email}, {phone}, {age}, {gender}, {marital_status}')

        if self.get_customer_by_username(username):
            logger.info(f'Username {username} already exists')
            raise BadRequest(f'Username {username} already exists')

        if self.get_customer_by_email(email):
            logger.info(f'Email {email} already exists')
            raise BadRequest(f'Email {email} already exists')

        phone = format_phone(phone)

        if self.get_customer_by_phone(phone):
            logger.info(f'Phone number {phone} already exists')
            raise BadRequest(f'Phone number {phone} already exists')

        customer = Customer(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, age=age, gender=gender, marital_status=marital_status)
        customer.set_password(password)
        self.db_session.add(customer)
        self.db_session.commit()

        logger.info(f'Customer registered successfully')
        
        access_token = create_access_token(identity=customer.username)
        refresh_token = create_refresh_token(identity=customer.username)

        logger.info(f'Access: {access_token}, Refresh: {refresh_token}')
        return {'access': access_token, 'refresh': refresh_token}
    
    def login_customer(self, data):
        logger.info('Enter login customer service')
        identifier = data.get('identifier')
        password = data.get('password')

        customer = self.get_customer(identifier)

        if not customer.check_password(password):
            logger.info(f'Invalid password for customer with username or email: {identifier}')
            raise AuthenticationError(f'Invalid password for customer with username or email: {identifier}')

        access_token = create_access_token(identity=customer.username)
        refresh_token = create_refresh_token(identity=customer.username)

        logger.info(f'Access: {access_token}, Refresh: {refresh_token}')
        return {'access': access_token, 'refresh': refresh_token}

    def logout_customer(self, customer_username):
        logger.info('Enter logout customer service')
        customer = self.get_customer(customer_username)
        customer.last_logout = get_utc_now()
        self.db_session.commit()
        logger.info('Customer logged out successfully')
        return {'message': 'Customer logged out successfully'}
    
    def update_customer(self, customer_username, data):
        logger.info('Enter update customer service')
        customer = self.get_customer(customer_username)
        for key, value in data.items():
            setattr(customer, key, value)
        self.db_session.commit()
        logger.info('Customer updated successfully')
        return {'message': 'Customer updated successfully'}

    def get_customer_info(self, customer_username):
        logger.info('Enter get customer info service')
        customer = self.get_customer(customer_username)
        logger.info('Customer info retrieved successfully')
        return customer.to_dict()
