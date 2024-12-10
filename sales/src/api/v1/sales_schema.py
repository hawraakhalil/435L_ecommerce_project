from marshmallow import Schema, fields, validates_schema, ValidationError, validate

class PurchaseSchema(Schema):
    item_ids_or_names = fields.List(fields.String(), required=True)
    item_quantities = fields.List(fields.Integer(), required=True)

    @validates_schema
    def validate_items_and_quantities(self, data, **kwargs):
        item_ids_or_names = data.get('item_ids_or_names', [])
        item_quantities = data.get('item_quantities', [])

        if len(item_ids_or_names) != len(item_quantities):
            raise ValidationError('The number of item IDs/names must match the number of quantities.')

        if not all(x.isdigit() for x in item_ids_or_names) and not all(not x.isdigit() for x in item_ids_or_names):
            raise ValidationError('All identifiers must be either all IDs or all names.')

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
