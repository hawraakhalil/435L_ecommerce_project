from shared.models.BaseModel import BaseModel
from shared.db import db

class Item(BaseModel, db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(255), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    reviews = db.relationship('Review', back_populates='item')
    transactions = db.relationship('Transaction', secondary='transaction_items', back_populates='items')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price_per_unit': self.price_per_unit,
            'currency': self.currency,
            'quantity': self.quantity,
            'description': self.description
        }
