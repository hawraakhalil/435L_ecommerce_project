"""
reviews.models.item
===================

This module defines the `Item` class, which represents item data in the database.

Classes
-------
Item
    A database model for storing item-related information.
"""

from reviews.src.extensions import db


class Item(db.Model):
    """
    A database model representing an item.

    Attributes
    ----------
    id : int
        Unique identifier for the item.
    name : str
        Name of the item (unique and required).
    category : str
        Category of the item (required).
    price_per_unit : float
        Price per unit of the item (required).
    currency : str
        Currency of the item's price (required).
    quantity : int
        Quantity of the item available in inventory (required).
    description : str
        Description of the item (required).

    Methods
    -------
    to_dict()
        Converts the item's attributes to a dictionary format.
    """

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    category = db.Column(db.String(255), nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def to_dict(self) -> dict:
        """
        Converts the item's attributes to a dictionary format.

        Returns
        -------
        dict
            A dictionary representation of the item's attributes.
        """
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price_per_unit': self.price_per_unit,
            'currency': self.currency,
            'quantity': self.quantity,
            'description': self.description
        }
