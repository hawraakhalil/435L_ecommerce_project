"""
admin.models
============

This module defines the `Customer` class, which represents customer data in the database.

Classes
-------
Customer
    A database model for storing customer-related information.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from admin.src.extensions import db
from admin.src.utils.utils import get_utc_now


class Customer(db.Model):
    """
    A database model representing a customer.

    Attributes
    ----------
    id : int
        Unique identifier for the customer.
    username : str
        Unique username for the customer.
    email : str
        Customer's email address.
    password : str
        Hashed password for the customer.
    first_name : str
        Customer's first name.
    last_name : str
        Customer's last name.
    phone : str
        Customer's phone number.
    age : int
        Customer's age.
    gender : str
        Customer's gender.
    marital_status : str
        Customer's marital status.
    lbp_balance : float
        Customer's balance in Lebanese Pounds (LBP).
    usd_balance : float
        Customer's balance in US Dollars (USD).
    status : str
        Account status (e.g., 'active').
    last_logout : datetime, optional
        Timestamp of the customer's last logout.
    items : JSON
        List of items associated with the customer.
    created_at : datetime
        Timestamp of the customer's account creation.

    Methods
    -------
    set_password(password)
        Hashes and sets the customer's password.
    check_password(password)
        Verifies if the given password matches the stored hashed password.
    to_dict()
        Converts the customer's attributes to a dictionary format.
    """

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
    lbp_balance = db.Column(db.Float, nullable=False, default=0)
    usd_balance = db.Column(db.Float, nullable=False, default=0)
    status = db.Column(db.String(255), nullable=False, default='active')
    last_logout = db.Column(db.DateTime, nullable=True)
    items = db.Column(db.JSON, nullable=False, default=[])

    created_at = db.Column(db.DateTime, default=get_utc_now, nullable=False)

    def set_password(self, password: str) -> None:
        """
        Hashes and sets the customer's password.

        Parameters
        ----------
        password : str
            The plain-text password to hash.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifies if the given password matches the stored hashed password.

        Parameters
        ----------
        password : str
            The plain-text password to check.

        Returns
        -------
        bool
            `True` if the password matches, `False` otherwise.
        """
        return check_password_hash(self.password, password)

    def to_dict(self) -> dict:
        """
        Converts the customer's attributes to a dictionary format.

        Returns
        -------
        dict
            A dictionary representation of the customer's attributes.
        """
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
