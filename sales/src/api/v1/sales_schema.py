from marshmallow import Schema, fields

from marshmallow import Schema, fields, validates_schema, ValidationError

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
    transaction_id = fields.Integer()
