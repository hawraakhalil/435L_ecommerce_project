from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.exceptions import NotFound, BadRequest

from admin.src.model.AdminsModel import Admin
from admin.src.utils.errors import AuthenticationError
from admin.src.utils.utils import get_utc_now, format_phone
from admin.src.utils.logger import logger


class AdminService:
    def __init__(self, db_session):
        self.db_session = db_session

    @staticmethod
    def get_admin_by_username(username):
        return Admin.query.filter(Admin.username == username).first()

    @staticmethod
    def get_admin_by_email(email):
        return Admin.query.filter(Admin.email == email).first()
    
    @staticmethod
    def get_admin_by_phone(phone):
        return Admin.query.filter(Admin.phone == phone).first()
    
    @staticmethod
    def get_admin_by_id(admin_id):
        return Admin.query.filter(Admin.id == admin_id).first()

    def get_admin(self, identifier):
        admin = self.get_admin_by_username(identifier) or self.get_admin_by_email(identifier) or self.get_admin_by_phone(identifier) or self.get_admin_by_id(identifier)
        if not admin:
            logger.info(f'Admin with identifier {identifier} not found')
            raise NotFound(f'Admin with identifier {identifier} not found')
        return admin
    
    def register_admin(self, data):
        logger.info('Enter register admin service')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')
        gender = data.get('gender')
        marital_status = data.get('marital_status')

        logger.info(f'Registering admin with username: {username}, email: {email}, phone: {phone}, age: {age}, gender: {gender}, marital_status: {marital_status}')

        if self.get_admin_by_username(username):
            logger.info(f'Username {username} already exists')
            raise BadRequest(f'Username {username} already exists')

        if self.get_admin_by_email(email):
            logger.info(f'Email {email} already exists')
            raise BadRequest(f'Email {email} already exists')

        phone = format_phone(phone)

        if self.get_admin_by_phone(phone):
            logger.info(f'Phone number {phone} already exists')
            raise BadRequest(f'Phone number {phone} already exists')

        admin = Admin(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, age=age, gender=gender, marital_status=marital_status)
        admin.set_password(password)
        self.db_session.add(admin)
        self.db_session.commit()

        logger.info('Admin registered successfully')
        
        access_token = create_access_token(identity=str(admin.username))
        refresh_token = create_refresh_token(identity=str(admin.username))

        logger.info(f'Access: {access_token}, Refresh: {refresh_token}')
        return {'access': access_token, 'refresh': refresh_token}
    
    def login_admin(self, data):
        logger.info('Enter login admin service')
        identifier = data.get('identifier')
        password = data.get('password')

        logger.info(f'Logging in admin with identifier: {identifier}')
        admin = self.get_admin(identifier)

        if not admin.check_password(password):
            logger.info(f'Invalid password for admin with username or email: {identifier}')
            raise AuthenticationError(f'Invalid password for admin with username or email: {identifier}')

        access_token = create_access_token(identity=admin.username)
        refresh_token = create_refresh_token(identity=admin.username)

        return {'access': access_token, 'refresh': refresh_token}

    def logout_admin(self, admin_username):
        logger.info('Enter logout admin service')
        admin = self.get_admin(admin_username)
        admin.last_logout = get_utc_now()
        self.db_session.commit()
        logger.info('Admin logged out successfully')
        return {'message': 'Admin logged out successfully'}
    
    def update_admin(self, admin_username, data):
        logger.info('Enter update admin service')
        admin = self.get_admin(admin_username)
        for key, value in data.items():
            setattr(admin, key, value)
        self.db_session.commit()
        logger.info('Admin updated successfully')
        return {'message': 'Admin updated successfully'}

    def get_admin_info(self, admin_username):
        logger.info('Enter get admin info service')
        admin = self.get_admin(admin_username)
        logger.info('Admin info retrieved successfully')
        return admin.to_dict()
