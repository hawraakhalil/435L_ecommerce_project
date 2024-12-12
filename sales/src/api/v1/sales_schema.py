from marshmallow import Schema, fields, validates_schema, ValidationError, validate

class PurchaseSchema(Schema):
    item_ids = fields.List(fields.Integer(), required=True)
    item_quantities = fields.List(fields.Integer(), required=True)

    @validates_schema
    def validate_items_and_quantities(self, data, **kwargs):
        if len(data['item_ids']) != len(data['item_quantities']):
            raise ValidationError('The number of item IDs must match the number of quantities.')

class ReversePurchaseSchema(Schema):
    transaction_id = fields.Integer(required=True)

class ItemSchema(Schema):
    item_id = fields.Integer(validate=validate.Range(min=1))
    name = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_item_id(self, data, **kwargs):
        if not data.get('item_id') and not data.get('name'):
            raise ValidationError('Either item id or name must be provided')
        if data.get('item_id') and data.get('name'):
            raise ValidationError('Either item id or name must be provided, not both')
