"""
reviews.schemas
===============

This module defines Marshmallow schemas for validating review-related input data.

Schemas
-------
- `AddReviewSchema`: Validation schema for adding a review.
- `UpdateReviewSchema`: Validation schema for updating a review.
- `GetCustomerReviewsSchema`: Validation schema for fetching customer reviews.
- `ReviewSchema`: Validation schema for identifying a specific review.
"""

from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class AddReviewSchema(Schema):
    """
    Validation schema for adding a review.

    Attributes
    ----------
    item_id : int, optional
        The ID of the item being reviewed.
    name : str, optional
        The name of the item being reviewed.
    rating : float
        The rating given to the item (required, between 1 and 5).
    comment : str
        The review comment (required).

    Methods
    -------
    validate_item_id(data, **kwargs)
        Ensures that either `item_id` or `name` is provided, but not both.
    """
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    rating = fields.Float(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.String(required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        """
        Ensures that either `item_id` or `name` is provided, but not both.

        Raises
        ------
        ValidationError
            If neither or both fields are provided.
        """
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')


class UpdateReviewSchema(Schema):
    """
    Validation schema for updating a review.

    Attributes
    ----------
    item_id : int, optional
        The ID of the item being reviewed.
    name : str, optional
        The name of the item being reviewed.
    rating : float, optional
        The updated rating (between 1 and 5).
    comment : str, optional
        The updated review comment.

    Methods
    -------
    validate_review(data, **kwargs)
        Ensures that either `item_id` or `name` is provided, and at least one of `rating` or `comment` is provided.
    """
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    rating = fields.Float(validate=validate.Range(min=1, max=5))
    comment = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_review(self, data, **kwargs):
        """
        Ensures that either `item_id` or `name` is provided, and at least one of `rating` or `comment` is provided.

        Raises
        ------
        ValidationError
            If neither or both fields are provided, or if `rating` and `comment` are both missing.
        """
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
        if not data.get('rating') and not data.get('comment'):
            raise ValidationError('Rating and/or comment are required')


class GetCustomerReviewsSchema(Schema):
    """
    Validation schema for fetching customer reviews.

    Attributes
    ----------
    customer_username : str, optional
        The username of the customer whose reviews are being fetched.
    customer_email : str, optional
        The email of the customer whose reviews are being fetched.

    Methods
    -------
    validate_customer(data, **kwargs)
        Ensures that either `customer_username` or `customer_email` is provided, but not both.
    """
    customer_username = fields.String(validate=validate.Length(min=1))
    customer_email = fields.Email(validate=validate.Length(min=1))

    @validates_schema
    def validate_customer(self, data, **kwargs):
        """
        Ensures that either `customer_username` or `customer_email` is provided, but not both.

        Raises
        ------
        ValidationError
            If neither or both fields are provided.
        """
        if not data.get('customer_username') and not data.get('customer_email'):
            raise ValidationError('Either customer username or email must be provided')
        if data.get('customer_username') and data.get('customer_email'):
            raise ValidationError('Either customer username or email must be provided, not both')


class ReviewSchema(Schema):
    """
    Validation schema for identifying a specific review.

    Attributes
    ----------
    item_id : int, optional
        The ID of the item being reviewed.
    name : str, optional
        The name of the item being reviewed.

    Methods
    -------
    validate_item_id(data, **kwargs)
        Ensures that either `item_id` or `name` is provided, but not both.
    """
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        """
        Ensures that either `item_id` or `name` is provided, but not both.

        Raises
        ------
        ValidationError
            If neither or both fields are provided.
        """
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
