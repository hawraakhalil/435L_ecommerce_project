"""
admin.models
============

This module defines the `Transaction` class, which represents transaction data in the database.

Classes
-------
Transaction
    A database model for storing transaction-related information.
"""

from admin.src.extensions import db


class Transaction(db.Model):
    """
    A database model representing a transaction.

    Attributes
    ----------
    id : int
        Unique identifier for the transaction.
    customer_id : int
        The ID of the customer associated with the transaction.
    items : JSON
        A list of items involved in the transaction.
    items_quantities : JSON
        A list of quantities corresponding to the items in the transaction.
    lbp_total_price : float
        The total price of the transaction in Lebanese Pounds (LBP).
    usd_total_price : float
        The total price of the transaction in US Dollars (USD).
    status : str
        The status of the transaction (e.g., 'completed').

    Methods
    -------
    to_dict()
        Converts the transaction's attributes to a dictionary format.
    """

    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    items = db.Column(db.JSON, nullable=False, default=[])
    items_quantities = db.Column(db.JSON, nullable=False, default=[])
    lbp_total_price = db.Column(db.Float, nullable=False)
    usd_total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255), nullable=False, default='completed')

    def to_dict(self) -> dict:
        """
        Converts the transaction's attributes to a dictionary format.

        Returns
        -------
        dict
            A dictionary representation of the transaction's attributes.
        """
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'items': self.items,
            'items_quantities': self.items_quantities,
            'lbp_total_price': self.lbp_total_price,
            'usd_total_price': self.usd_total_price,
            'status': self.status
        }
