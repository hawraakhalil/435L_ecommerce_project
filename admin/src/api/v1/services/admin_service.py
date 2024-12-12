from flask_jwt_extended import create_access_token, create_refresh_token

from shared.models.AdminsModel import Admin
from admin.src.errors import AuthenticationError
from werkzeug.exceptions import NotFound
from shared.utils.utils import get_utc_now, format_phone


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
            raise NotFound(f'Admin with identifier {identifier} not found')
        return admin
    
    def register_admin(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        phone = data.get('phone')
        age = data.get('age')
        gender = data.get('gender')
        marital_status = data.get('marital_status')

        if self.get_admin_by_username(username):
            raise ValueError(f'Username {username} already exists')

        if self.get_admin_by_email(email):
            raise ValueError(f'Email {email} already exists')

        phone = format_phone(phone)

        if self.get_admin_by_phone(phone):
            raise ValueError(f'Phone number {phone} already exists')

        admin = Admin(first_name=first_name, last_name=last_name, username=username, email=email, phone=phone, age=age, gender=gender, marital_status=marital_status)
        admin.set_password(password)
        self.db_session.add(admin)
        self.db_session.commit()
        
        access_token = create_access_token(identity=admin.id)
        refresh_token = create_refresh_token(identity=admin.id)

        return {'access': access_token, 'refresh': refresh_token}
    
    def login_admin(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        admin = self.get_admin(identifier)

        if not admin.check_password(password):
            raise AuthenticationError(f'Invalid password for admin with username or email: {identifier}')

        access_token = create_access_token(identity=admin.id)
        refresh_token = create_refresh_token(identity=admin.id)

        return {'access': access_token, 'refresh': refresh_token}

    def logout_admin(self, admin_id):
        admin = self.get_admin(admin_id)
        admin.last_logout = get_utc_now()
        self.db_session.commit()
        return {'message': 'Admin logged out successfully'}
    
    def update_admin(self, admin_id, data):
        admin = self.get_admin(admin_id)
        for key, value in data.items():
            setattr(admin, key, value)
        self.db_session.commit()
        return {'message': 'Admin updated successfully'}

    def get_admin_info(self, admin_id):
        admin = self.get_admin(admin_id)
        return admin.to_dict()
