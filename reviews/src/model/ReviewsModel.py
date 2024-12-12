from reviews.src.extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at,
        }
