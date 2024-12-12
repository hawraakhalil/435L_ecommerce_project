from werkzeug.security import generate_password_hash, check_password_hash
from admin.src.extensions import db
from admin.src.utils.utils import get_utc_now

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    marital_status = db.Column(db.String(255), nullable=False)
    lbp_balance = db.Column(db.Float, nullable=False, default=0)
    usd_balance = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(255), nullable=False, default='active')
    last_logout = db.Column(db.DateTime, nullable=True)
    items = db.Column(db.JSON, nullable=False)

    created_at = db.Column(db.DateTime, default=get_utc_now, nullable=False)

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
            'lbp_balance': self.lbp_balance,
            'usd_balance': self.usd_balance,
            'status': self.status,
            'created_at': self.created_at
        }
