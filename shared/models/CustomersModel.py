from werkzeug.security import generate_password_hash, check_password_hash
from src.models.BaseModel import BaseModel
from shared.db import db

class Customer(BaseModel, db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    marital_status = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    last_logout = db.Column(db.DateTime, nullable=True)

    transactions = db.relationship('Transaction', back_populates='customer')
    reviews = db.relationship('Review', back_populates='customer')
    items = db.relationship('Item', secondary='transaction_items', back_populates='customers')

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'marital_status': self.marital_status,
            'balance': self.balance,
            'created_at': self.created_at
        }
