from sales.src.extensions import db

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(255), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

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
