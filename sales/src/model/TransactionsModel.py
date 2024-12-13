from src.extensions import db

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.JSON, nullable=False, default=[])
    items_quantities = db.Column(db.JSON, nullable=False, default=[])
    lbp_total_price = db.Column(db.Float, nullable=False)
    usd_total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False, default='completed')

    def to_dict(self):
        return {
            'id': self.id,
            'items': self.items,
            'customer_id': self.customer_id,
            'items_quantities': self.items_quantities,
            'lbp_total_price': self.lbp_total_price,
            'usd_total_price': self.usd_total_price,
            'status': self.status
        }
