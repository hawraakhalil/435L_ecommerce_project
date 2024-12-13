"""
admin.customer_management_schemas
=================================

This module defines Marshmallow schemas for validating customer management-related input data.

Schemas
-------
- `TopUpCustomerSchema`: Validation schema for topping up a customer's balance.
- `UpdateCustomerProfileSchema`: Validation schema for updating a customer's profile.
- `CustomerSchema`: Validation schema for identifying a customer.
- `ReverseTransactionSchema`: Validation schema for reversing a transaction.
"""

from marshmallow import Schema, fields, validate, ValidationError


class TopUpCustomerSchema(Schema):
    """
    Validation schema for topping up a customer's balance.

    Attributes
    ----------
    customer_id : int
        The ID of the customer to be topped up (required).
    amount : float
        The amount to be added to the customer's balance (required, minimum 0.01).
    currency : str
        The currency of the top-up amount (required, one of 'LBP', 'USD').
    """
    customer_id = fields.Integer(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.String(required=True, validate=validate.OneOf(['LBP', 'USD']))


class UpdateCustomerProfileSchema(Schema):
    """
    Validation schema for updating a customer's profile.

    Attributes
    ----------
    customer_id : int
        The ID of the customer to be updated (required).
    first_name : str, optional
        The updated first name of the customer.
    last_name : str, optional
        The updated last name of the customer.
    phone : str, optional
        The updated phone number of the customer (must be 8 digits).
    age : int, optional
        The updated age of the customer (must be between 18 and 150).
    gender : str, optional
        The updated gender of the customer (one of 'male', 'female', 'other').
    marital_status : str, optional
        The updated marital status of the customer (one of 'single', 'married', 'divorced', 'widowed').
    """
    customer_id = fields.Integer(required=True)
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    phone = fields.String(validate=[validate.Length(equal=8), validate.Regexp(r'^\d{8}$')])
    age = fields.Integer(validate=validate.Range(min=18, max=150))
    gender = fields.String(validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))


class CustomerSchema(Schema):
    """
    Validation schema for identifying a customer.

    Attributes
    ----------
    customer_id : int
        The ID of the customer (required).
    """
    customer_id = fields.Integer(required=True)


class ReverseTransactionSchema(Schema):
    """
    Validation schema for reversing a transaction.

    Attributes
    ----------
    transaction_id : int
        The ID of the transaction to be reversed (required).
    """
    transaction_id = fields.Integer(required=True)
