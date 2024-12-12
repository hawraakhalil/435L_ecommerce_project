from flask_jwt_extended import create_access_token, create_refresh_token
from shared.models.CustomersModel import Customer
from customers.src.errors import AuthenticationError
from werkzeug.exceptions import NotFound
from shared.utils.utils import get_utc_now, format_phone


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
            raise NotFound(f'Customer with identifier {identifier} not found')
        return customer
    
    def is_customer_banned(customer_id):
        customer = Customer.query.filter(Customer.id == customer_id).first()
        if not customer:
            return True
        return customer.is_banned
    
    def register_customer(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')
        gender = data.get('gender')
        marital_status = data.get('marital_status')

        if self.get_customer_by_username(username):
            raise ValueError(f'Username {username} already exists')

        if self.get_customer_by_email(email):
            raise ValueError(f'Email {email} already exists')

        phone = format_phone(phone)

        if self.get_customer_by_phone(phone):
            raise ValueError(f'Phone number {phone} already exists')

        customer = Customer(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, age=age, gender=gender, marital_status=marital_status)
        customer.set_password(password)
        self.db_session.add(customer)
        self.db_session.commit()
        
        access_token = create_access_token(identity=customer.id)
        refresh_token = create_refresh_token(identity=customer.id)

        return {'access': access_token, 'refresh': refresh_token}
    
    def login_customer(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        customer = self.get_customer(identifier)

        if not customer.check_password(password):
            raise AuthenticationError(f'Invalid password for customer with username or email: {identifier}')

        access_token = create_access_token(identity=customer.id)
        refresh_token = create_refresh_token(identity=customer.id)

        return {'access': access_token, 'refresh': refresh_token}

    def logout_customer(self, customer_id):
        customer = self.get_customer(customer_id)
        customer.last_logout = get_utc_now()
        self.db_session.commit()
        return {'message': 'Customer logged out successfully'}
    
    def update_customer(self, customer_id, data):
        customer = self.get_customer(customer_id)
        for key, value in data.items():
            setattr(customer, key, value)
        self.db_session.commit()
        return {'message': 'Customer updated successfully'}

    def get_customer_info(self, customer_id):
        customer = self.get_customer(customer_id)
        return customer.to_dict()
