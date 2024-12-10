from src.models.TransactionsModel import Transaction
from src.models.ItemsModel import Item
from src.models.CustomersModel import Customer

class SalesService:
    def __init__(self, db_session):
        self.db_session = db_session

    def purchase(self, data, user_id):
        item_ids_or_names = data.get('item_ids_or_names', [])
        item_quantities = data.get('item_quantities', [])

        

    def reverse_purchase(self, data):
        pass

    def get_transactions(self):
        pass


