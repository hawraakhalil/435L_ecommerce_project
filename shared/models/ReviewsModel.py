from shared.models.BaseModel import BaseModel
from shared.db import db

class Review(BaseModel, db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    item = db.relationship('Item', back_populates='reviews', cascade="all, delete-orphan")
    customer = db.relationship('Customer', back_populates='reviews', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'review': self.review,
            'rating': self.rating,
            'item_id': self.item_id,
            'customer_id': self.customer_id
        }
