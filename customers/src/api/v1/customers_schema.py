"""
customers.schemas
=================

This module defines Marshmallow schemas for validating customer-related input data.

Schemas
-------
- `RegisterCustomerSchema`: Validation schema for customer registration.
- `LoginCustomerSchema`: Validation schema for customer login.
- `UpdateCustomerSchema`: Validation schema for updating customer details.
"""

from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class RegisterCustomerSchema(Schema):
    """
    Validation schema for registering a new customer.

    Attributes
    ----------
    first_name : str
        Customer's first name (required, non-empty).
    last_name : str
        Customer's last name (required, non-empty).
    username : str
        Unique username for the customer (required, non-empty).
    password : str
        Password for the customer (required, minimum 8 characters).
    email : str
        Valid email address (required).
    phone : str
        Customer's phone number (required, 8 digits).
    age : int
        Customer's age (required, between 18 and 150).
    gender : str
        Customer's gender (required, one of 'male', 'female', 'other').
    marital_status : str
        Customer's marital status (required, one of 'single', 'married', 'divorced', 'widowed').
    """
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8))
    email = fields.Email(required=True)
    phone = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=8),
            validate.Regexp(r'^\d{8}$')
        ]
    )
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=150))
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(required=True, validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))


class LoginCustomerSchema(Schema):
    """
    Validation schema for customer login.

    Attributes
    ----------
    identifier : str
        Customer's username or email (required, non-empty).
    password : str
        Customer's password (required, minimum 8 characters).
    """
    identifier = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8))


class UpdateCustomerSchema(Schema):
    """
    Validation schema for updating customer details.

    Attributes
    ----------
    first_name : str, optional
        Customer's updated first name (non-empty).
    last_name : str, optional
        Customer's updated last name (non-empty).
    phone : str, optional
        Customer's updated phone number (8 digits).
    age : int, optional
        Customer's updated age (between 18 and 150).
    gender : str, optional
        Customer's updated gender (one of 'male', 'female', 'other').
    marital_status : str, optional
        Customer's updated marital status (one of 'single', 'married', 'divorced', 'widowed').

    Methods
    -------
    validate_update(data)
        Validates that at least one field is provided for an update.
    """
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    phone = fields.String(
        validate=[
            validate.Length(min=8, max=8),
            validate.Regexp(r'^\d{8}$')
        ]
    )
    age = fields.Integer(validate=validate.Range(min=18, max=150))
    gender = fields.String(validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))

    @validates_schema
    def validate_update(self, data, **kwargs):
        """
        Validates that at least one field is provided for updating customer details.

        Parameters
        ----------
        data : dict
            The input data being validated.

        Raises
        ------
        ValidationError
            If no fields are provided in the input data.
        """
        if not any(data.values()):
            raise ValidationError('At least one field must be provided for update')
