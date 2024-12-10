from shared.models.BaseModel import BaseModel
from sqlalchemy.sql.schema import ForeignKey
from shared.db import db

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    review = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)

    item = db.relationship('Item', back_populates='reviews')
    customer = db.relationship('Customer', back_populates='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'review': self.review,
            'rating': self.rating,
            'item_id': self.item_id,
            'comment': self.comment,
            'created_at': self.created_at,
        }
