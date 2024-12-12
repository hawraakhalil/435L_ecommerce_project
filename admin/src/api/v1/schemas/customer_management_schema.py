from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class TopUpCustomerSchema(Schema):
    customer_id = fields.Integer(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    currency = fields.String(required=True, validate=validate.OneOf(['LBP', 'USD']))

class UpdateCustomerProfileSchema(Schema):
    customer_id = fields.Integer(required=True)
    first_name = fields.String(validate=validate.Length(min=1))
    last_name = fields.String(validate=validate.Length(min=1))
    phone = fields.String(validate=[validate.Length(equal=8), validate.Regexp(r'^\d{8}$')])
    age = fields.Integer(validate=validate.Range(min=18, max=150))
    gender = fields.String(validate=validate.OneOf(['male', 'female', 'other']))
    marital_status = fields.String(validate=validate.OneOf(['single', 'married', 'divorced', 'widowed']))

class CustomerSchema(Schema):
    customer_id = fields.Integer(required=True)

class ReverseTransactionSchema(Schema):
    transaction_id = fields.Integer(required=True)
