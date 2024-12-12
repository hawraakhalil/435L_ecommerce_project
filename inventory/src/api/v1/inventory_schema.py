from marshmallow import Schema, fields, validate, ValidationError, validates_schema

class AddItemSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(required=True, validate=validate.OneOf(['food', 'drinks', 'clothes', 'electronics', 'accessories', 'household', 'pets', 'mobiles', 'furniture', 'toys', 'kids', 'beauty', 'books', 'sports', 'other']))
    price_per_unit = fields.Integer(required=True, validate=validate.Range(min=1))
    currency = fields.String(required=True, validate=validate.OneOf(['USD', 'LBP']))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    description = fields.String(required=True, validate=validate.Length(min=1))

class RestockItemSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')

class UpdateItemSchema(Schema):
    name = fields.String(validate=validate.Length(min=1))
    category = fields.String(validate=validate.OneOf(['food', 'drinks', 'clothes', 'electronics', 'accessories', 'household', 'pets', 'mobiles', 'furniture', 'toys', 'kids', 'beauty', 'books', 'sports', 'other']))
    price_per_unit = fields.Integer(validate=validate.Range(min=1))
    currency = fields.String(validate=validate.OneOf(['USD', 'LBP']))
    quantity = fields.Integer(validate=validate.Range(min=1))
    description = fields.String(validate=validate.Length(min=1))

class ItemSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')

class UpdateItemSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))
    category = fields.String(validate=validate.OneOf(['food', 'drinks', 'clothes', 'electronics', 'accessories', 'household', 'pets', 'mobiles', 'furniture', 'toys', 'kids', 'beauty', 'books', 'sports', 'other']))
    price_per_unit = fields.Integer(validate=validate.Range(min=1))
    currency = fields.String(validate=validate.OneOf(['USD', 'LBP']))
    quantity = fields.Integer(validate=validate.Range(min=1))
    description = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
        if not data.get('category') and not data.get('price_per_unit') and not data.get('currency') and not data.get('quantity') and not data.get('description'):
            raise ValidationError('At least one field must be provided')

class CategorySchema(Schema):
    category = fields.String(required=True, validate=validate.OneOf(['food', 'drinks', 'clothes', 'electronics', 'accessories', 'household', 'pets', 'mobiles', 'furniture', 'toys', 'kids', 'beauty', 'books', 'sports', 'other']))
