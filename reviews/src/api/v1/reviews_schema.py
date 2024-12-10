from marshmallow import Schema, fields, validate, ValidationError, validates_schema


class AddReviewSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    rating = fields.Float(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.String(required=True, validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')

class UpdateReviewSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    rating = fields.Float(validate=validate.Range(min=1, max=5))
    comment = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_review(self, data, **kwargs):
        if not data.get('item_id') or not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
        if not data.get('rating') and not data.get('comment'):
            raise ValidationError('Rating and/or comment are required')

class GetCustomerReviewsSchema(Schema):
    customer_username = fields.String(validate=validate.Length(min=1))
    customer_email = fields.Email(validate=validate.Length(min=1))

    @validates_schema
    def validate_customer(self, data, **kwargs):
        if not data.get('customer_username') and not data.get('customer_email'):
            raise ValidationError('Either customer username or email must be provided')
        if data.get('customer_username') and data.get('customer_email'):
            raise ValidationError('Either customer username or email must be provided, not both')

class ReviewSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
