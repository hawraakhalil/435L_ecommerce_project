from shared.models.CustomersModel import Customer
from shared.models.ReviewsModel import Review
from shared.models.ItemsModel import Item


from werkzeug.exceptions import NotFound, BadRequest

class ReviewsService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_customer(self, customer_id):
        customer = Customer.query.filter_by(id=customer_id).first()
        if not customer:
            raise NotFound(f'Customer with id {customer_id} not found')
        return customer
    
    def get_customer_by_username_or_email(self, username, email):
        customer = Customer.query.filter_by(username=username).first() or Customer.query.filter_by(email=email).first()
        if not customer:
            raise NotFound(f'Customer with username or email {username or email} not found')
        return customer

    def get_item(self, item_id, name):
        item = Item.query.filter_by(id=item_id).first() or Item.query.filter_by(name=name).first()
        if not item:
            raise NotFound(f'Item with id or name {item_id or name} not found')
        return item
    
    def get_review(self, customer_id, item_id):
        review = Review.query.filter_by(customer_id=customer_id, item_id=item_id).first()
        if not review:
            raise NotFound(f'Review for item {review.item.name} by customer {review.customer.username} not found')
        return review

    def add_review(self, data, customer_id):
        item_id = data.get('item_id')
        name = data.get('name')
        rating = data.get('rating')
        comment = data.get('comment')

        customer = self.get_customer(customer_id)
        item = self.get_item(item_id, name)

        if item not in customer.items:
            raise BadRequest(f'Customer {customer.username} has not purchased item {item.name}')

        review = Review(
            customer=customer,
            item=item,
            rating=rating,
            comment=comment
        )

        self.db_session.add(review)
        self.db_session.commit()

        return review.to_dict()

    def update_review(self, data, customer_id):
        item_id = data.get('item_id')
        name = data.get('name')
        rating = data.get('rating')
        comment = data.get('comment')

        customer = self.get_customer(customer_id)
        item = self.get_item(item_id, name)

        if item not in customer.items:
            raise BadRequest(f'Customer {customer.username} has not purchased item {item.name}')
        
        review = self.get_review(customer_id, item_id)
        
        if rating:
            review.rating = rating
        if comment:
            review.comment = comment
        
        self.db_session.commit()
        return review.to_dict()

    def delete_review(self, data, customer_id):
        item_id = data.get('item_id')
        name = data.get('name')

        customer = self.get_customer(customer_id)
        item = self.get_item(item_id, name)

        review = self.get_review(customer_id, item_id)
        self.db_session.delete(review)
        self.db_session.commit()
        return {'message': f'Review for item {item.name} by customer {customer.username} deleted successfully'}

    def get_customer_reviews(self, data):
        customer_username = data.get('customer_username')
        customer_email = data.get('customer_email')

        customer = self.get_customer_by_username_or_email(customer_username, customer_email)
        return [review.to_dict() for review in customer.reviews]
    
    def get_item_reviews(self, data):
        item_name = data.get('item_name')
        item_id = data.get('item_id')
        item = self.get_item(item_id, item_name)
        return [review.to_dict() for review in item.reviews]

    @staticmethod
    def get_all_reviews():
        return [review.to_dict() for review in Review.query.all()]