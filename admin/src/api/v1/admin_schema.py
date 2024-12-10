from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class RegisterAdminSchema(Schema):
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
    identifier = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.String(required=True, validate=validate.Length(min=8))

class UpdateAdminSchema(Schema):
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
        if not any(data.values()):
            raise ValidationError('At least one field must be provided for update')
