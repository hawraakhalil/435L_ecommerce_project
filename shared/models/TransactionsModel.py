from shared.db import db
from shared.models.BaseModel import BaseModel

class Transaction(BaseModel, db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    items_quantities = db.Column(db.JSON, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    
    item = db.relationship('Item', back_populates='transactions')
    customer = db.relationship('Customer', back_populates='transactions')

    def to_dict(self):
        return {
            'id': self.id,
            'item': self.item.to_dict(),
            'customer': self.customer.username,
            'items_quantities': self.items_quantities,
            'total_price': self.total_price,
            'created_at': self.created_at
        }
