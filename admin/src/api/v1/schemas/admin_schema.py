"""
admin.schemas
=============

This module defines Marshmallow schemas for validating admin-related input data.

Schemas
-------
- `RegisterAdminSchema`: Validation schema for registering a new admin.
- `LoginAdminSchema`: Validation schema for logging in an admin.
- `UpdateAdminSchema`: Validation schema for updating admin details.
"""

from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class RegisterAdminSchema(Schema):
    """
    Validation schema for registering a new admin.

    Attributes
    ----------
    first_name : str
        Admin's first name (required, non-empty).
    last_name : str
        Admin's last name (required, non-empty).
    username : str
        Unique username for the admin (required, non-empty).
    password : str
        Password for the admin (required, minimum 8 characters).
    email : str
        Valid email address (required).
    phone : str
        Admin's phone number (required, 8 digits).
    age : int
        Admin's age (required, between 18 and 150).
    gender : str
        Admin's gender (required, one of 'male', 'female', 'other').
    marital_status : str
        Admin's marital status (required, one of 'single', 'married', 'divorced', 'widowed').
    """
    first_name = fields.String(required=True, validate=validate.Length(min=1))
    last_name = fields.String(required=True, validate=validate.Length(min=1))
    username = fields.String(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8))
    email = fields.Email(required=True)
    phone = fields.String(
        required=True, 
        validate=[
            validate.Length(equal=8),
            validate.Regexp(r'^\d{8}$')
        ]
    )
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=150))
    gender = fields.String(required=True, validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(required=True, validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))


class LoginAdminSchema(Schema):
    """
    Validation schema for admin login.

    Attributes
    ----------
    identifier : str
        Admin's username or email (required, non-empty).
    password : str
        Admin's password (required, minimum 8 characters).
    """
    identifier = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8))


class UpdateAdminSchema(Schema):
    """
    Validation schema for updating admin details.

    Attributes
    ----------
    first_name : str, optional
        Admin's updated first name (non-empty).
    last_name : str, optional
        Admin's updated last name (non-empty).
    phone : str, optional
        Admin's updated phone number (8 digits).
    age : int, optional
        Admin's updated age (between 18 and 150).
    gender : str, optional
        Admin's updated gender (one of 'male', 'female', 'other').
    marital_status : str, optional
        Admin's updated marital status (one of 'single', 'married', 'divorced', 'widowed').

    Methods
    -------
    validate_update(data)
        Validates that at least one field is provided for an update.
    """
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    phone = fields.String(
        validate=[
            validate.Length(equal=8),
            validate.Regexp(r'^\d{8}$')
        ]
    )
    age = fields.Integer(validate=validate.Range(min=18, max=150))
    gender = fields.String(validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))

    @validates_schema
    def validate_update(self, data, **kwargs):
        """
        Validates that at least one field is provided for updating admin details.

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
