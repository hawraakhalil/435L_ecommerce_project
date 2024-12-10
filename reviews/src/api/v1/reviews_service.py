class ReviewsService:
    def __init__(self, db_session):
        self.db_session = db_session
    
    def add_review(self, data):
        item_id = data.get('item_id')
        name = data.get('name')
        rating = data.get('rating')
        comment = data.get('comment')

        customer 