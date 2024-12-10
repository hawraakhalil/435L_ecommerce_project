from shared.db import db
from shared.models.BaseModel import BaseModel

class Transaction(BaseModel, db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    items_quantities = db.Column(db.JSON, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    
    items = db.relationship('Item', secondary='transaction_items', back_populates='transactions', cascade="all, delete-orphan")
    customer = db.relationship('Customer', back_populates='transactions', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'items': [item.to_dict() for item in self.items],
            'customer': self.customer.username,
            'items_quantities': self.items_quantities,
            'total_price': self.total_price,
            'created_at': self.created_at
        }
