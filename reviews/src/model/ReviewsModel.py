"""
reviews.models.review
=====================

This module defines the `Review` class, which represents review data in the database.

Classes
-------
Review
    A database model for storing review-related information.
"""

from reviews.src.extensions import db


class Review(db.Model):
    """
    A database model representing a review.

    Attributes
    ----------
    id : int
        Unique identifier for the review.
    customer_id : int
        ID of the customer who wrote the review (required).
    item_id : int
        ID of the item being reviewed (required).
    rating : int
        Rating given to the item (required).
    comment : str, optional
        Additional comments provided by the customer.

    Methods
    -------
    to_dict()
        Converts the review's attributes to a dictionary format.
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=True)

    def to_dict(self) -> dict:
        """
        Converts the review's attributes to a dictionary format.

        Returns
        -------
        dict
            A dictionary representation of the review's attributes.
        """
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'item_id': self.item_id,
            'rating': self.rating,
            'comment': self.comment,
        }
