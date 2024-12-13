"""
admin.models
============

This module defines the `Admin` class, which represents admin data in the database.

Classes
-------
Admin
    A database model for storing admin-related information.
"""

from werkzeug.security import generate_password_hash, check_password_hash
from admin.src.extensions import db
from admin.src.utils.utils import get_utc_now


class Admin(db.Model):
    """
    A database model representing an admin.

    Attributes
    ----------
    id : int
        Unique identifier for the admin.
    username : str
        Unique username for the admin.
    email : str
        Admin's email address.
    password : str
        Hashed password for the admin.
    first_name : str
        Admin's first name.
    last_name : str
        Admin's last name.
    phone : str
        Admin's phone number.
    age : int
        Admin's age.
    gender : str
        Admin's gender.
    marital_status : str
        Admin's marital status.
    last_logout : datetime, optional
        Timestamp of the admin's last logout.
    created_at : datetime
        Timestamp of the admin's account creation.

    Methods
    -------
    set_password(password)
        Hashes and sets the admin's password.
    check_password(password)
        Verifies if the given password matches the stored hashed password.
    to_dict()
        Converts the admin's attributes to a dictionary format.
    """

    __tablename__ = 'admins'

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
    last_logout = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=get_utc_now, nullable=False)

    def set_password(self, password: str) -> None:
        """
        Hashes and sets the admin's password.

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
        Converts the admin's attributes to a dictionary format.

        Returns
        -------
        dict
            A dictionary representation of the admin's attributes.
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
            'created_at': self.created_at
        }
