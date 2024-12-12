from werkzeug.exceptions import NotFound, BadRequest

from reviews.src.model.CustomersModel import Customer
from reviews.src.model.ReviewsModel import Review
from reviews.src.model.ItemsModel import Item

from reviews.src.utils.logger import logger

class ReviewsService:
    def __init__(self, db_session):
        self.db_session = db_session
    
    @staticmethod
    def get_item_by_id(item_id):
        return Item.query.filter_by(id=item_id).first()
    
    @staticmethod
    def get_item_by_name(item_name):
        return Item.query.filter_by(name=item_name).first()
    
    @staticmethod
    def get_customer(username, email = None):
        customer = Customer.query.filter_by(username=username).first() or Customer.query.filter_by(email=email).first()
        if not customer:
            logger.info(f'Customer with username {username} or email {email} not found')
            raise NotFound(f'Customer with username {username} or email {email} not found')
        return customer

    def get_item(self, item_id, name):
        item = self.get_item_by_id(item_id) or self.get_item_by_name(name)
        if not item:
            logger.info(f'Item with id or name {item_id or name} not found')
            raise NotFound(f'Item with id or name {item_id or name} not found')
        return item
    
    def get_review(self, customer_username, item_id):
        review = Review.query.filter_by(customer_username=customer_username, item_id=item_id).first()
        if not review:
            logger.info(f'Review for item {review.item.name} by customer {review.customer.username} not found')
            raise NotFound(f'Review for item {review.item.name} by customer {review.customer.username} not found')
        return review

    def add_review(self, data, customer_username):
        item_id = data.get('item_id')
        name = data.get('name')
        rating = data.get('rating')
        comment = data.get('comment')

        customer = self.get_customer(customer_username)
        item = self.get_item(item_id, name)

        if item.to_dict() not in customer.items:
            logger.info(f'Customer {customer.username} has not purchased item {item.name}')
            raise BadRequest(f'Customer {customer.username} has not purchased item {item.name}')

        review = Review(
            customer_id=customer.id,
            item_id=item.id,
            rating=rating,
            comment=comment
        )

        self.db_session.add(review)
        self.db_session.commit()

        return review.to_dict()

    def update_review(self, data, customer_username):
        item_id = data.get('item_id')
        name = data.get('name')
        rating = data.get('rating')
        comment = data.get('comment')

        customer = self.get_customer(customer_username)
        item = self.get_item(item_id, name)
        review = self.get_review(customer.id, item.id)
        
        if rating:
            review.rating = rating
        if comment:
            review.comment = comment
        
        self.db_session.commit()
        return review.to_dict()

    def delete_review(self, data, customer_username):
        item_id = data.get('item_id')
        name = data.get('name')

        customer = self.get_customer(customer_username)
        item = self.get_item(item_id, name)
        review = self.get_review(customer.id, item.id)

        self.db_session.delete(review)
        self.db_session.commit()
        return {'message': f'Review for item {item.name} by customer {customer.username} deleted successfully'}

    def get_customer_reviews(self, data):
        customer_username = data.get('customer_username')
        customer_email = data.get('customer_email')

        customer = self.get_customer(customer_username, customer_email)
        reviews = Review.query.filter_by(customer_id=customer.id).all()
        return [review.to_dict() for review in reviews]
    
    def get_item_reviews(self, data):
        item_name = data.get('item_name')
        item_id = data.get('item_id')
        item = self.get_item(item_id, item_name)
        reviews = Review.query.filter_by(item_id=item.id).all()
        return [review.to_dict() for review in reviews]

    @staticmethod
    def get_all_reviews():
        return [review.to_dict() for review in Review.query.all()]
