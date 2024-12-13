"""
reviews.services
================

This module defines the `ReviewsService` class, which handles the business logic for managing reviews.

Classes
-------
ReviewsService
    A service class for managing reviews.
"""

from werkzeug.exceptions import NotFound, BadRequest

from reviews.src.model.CustomersModel import Customer
from reviews.src.model.ReviewsModel import Review
from reviews.src.model.ItemsModel import Item

from reviews.src.utils.logger import logger


class ReviewsService:
    """
    A service class for managing reviews.

    Methods
    -------
    get_item_by_id(item_id)
        Fetches an item by its ID.
    get_item_by_name(item_name)
        Fetches an item by its name.
    get_customer(username, email=None)
        Fetches a customer by username or email.
    get_item(item_id, name)
        Fetches an item by its ID or name.
    get_review(customer_username, item_id)
        Fetches a review by the customer username and item ID.
    add_review(data, customer_username)
        Adds a review for an item by a customer.
    update_review(data, customer_username)
        Updates an existing review.
    delete_review(data, customer_username)
        Deletes a review for an item by a customer.
    get_customer_reviews(data)
        Fetches all reviews made by a specific customer.
    get_item_reviews(data)
        Fetches all reviews for a specific item.
    get_all_reviews()
        Fetches all reviews in the system.
    """

    def __init__(self, db_session):
        """
        Initializes the ReviewsService with a database session.

        Parameters
        ----------
        db_session : SQLAlchemy session
            The database session to use for transactions.
        """
        self.db_session = db_session

    @staticmethod
    def get_item_by_id(item_id):
        """
        Fetches an item by its ID.

        Parameters
        ----------
        item_id : int
            The ID of the item to fetch.

        Returns
        -------
        Item
            The item if found, otherwise `None`.
        """
        return Item.query.filter_by(id=item_id).first()

    @staticmethod
    def get_item_by_name(item_name):
        """
        Fetches an item by its name.

        Parameters
        ----------
        item_name : str
            The name of the item to fetch.

        Returns
        -------
        Item
            The item if found, otherwise `None`.
        """
        return Item.query.filter_by(name=item_name).first()

    @staticmethod
    def get_customer(username, email=None):
        """
        Fetches a customer by username or email.

        Parameters
        ----------
        username : str
            The username of the customer.
        email : str, optional
            The email of the customer.

        Returns
        -------
        Customer
            The customer if found.

        Raises
        ------
        NotFound
            If no customer is found with the given username or email.
        """
        customer = Customer.query.filter_by(username=username).first() or Customer.query.filter_by(email=email).first()
        if not customer:
            logger.info(f'Customer with username {username} or email {email} not found')
            raise NotFound(f'Customer with username {username} or email {email} not found')
        return customer

    def get_item(self, item_id, name):
        """
        Fetches an item by its ID or name.

        Parameters
        ----------
        item_id : int, optional
            The ID of the item.
        name : str, optional
            The name of the item.

        Returns
        -------
        Item
            The item if found.

        Raises
        ------
        NotFound
            If no item is found.
        """
        item = self.get_item_by_id(item_id) or self.get_item_by_name(name)
        if not item:
            logger.info(f'Item with id or name {item_id or name} not found')
            raise NotFound(f'Item with id or name {item_id or name} not found')
        return item

    def get_review(self, customer_username, item_id):
        """
        Fetches a review by customer username and item ID.

        Parameters
        ----------
        customer_username : str
            The username of the customer who wrote the review.
        item_id : int
            The ID of the item being reviewed.

        Returns
        -------
        Review
            The review if found.

        Raises
        ------
        NotFound
            If no review is found.
        """
        review = Review.query.filter_by(customer_username=customer_username, item_id=item_id).first()
        if not review:
            logger.info(f'Review for item {review.item.name} by customer {review.customer.username} not found')
            raise NotFound(f'Review for item {review.item.name} by customer {review.customer.username} not found')
        return review

    def add_review(self, data, customer_username):
        """
        Adds a review for an item by a customer.

        Parameters
        ----------
        data : dict
            The review data.
        customer_username : str
            The username of the customer adding the review.

        Returns
        -------
        dict
            The newly created review's details.
        """
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
        """
        Updates an existing review.

        Parameters
        ----------
        data : dict
            The updated review data.
        customer_username : str
            The username of the customer updating the review.

        Returns
        -------
        dict
            The updated review's details.
        """
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
        """
        Deletes a review for an item by a customer.

        Parameters
        ----------
        data : dict
            The review identification data.
        customer_username : str
            The username of the customer deleting the review.

        Returns
        -------
        dict
            A message indicating the review was deleted successfully.
        """
        item_id = data.get('item_id')
        name = data.get('name')

        customer = self.get_customer(customer_username)
        item = self.get_item(item_id, name)
        review = self.get_review(customer.id, item.id)

        self.db_session.delete(review)
        self.db_session.commit()
        return {'message': f'Review for item {item.name} by customer {customer.username} deleted successfully'}

    def get_customer_reviews(self, data):
        """
        Fetches all reviews made by a specific customer.

        Parameters
        ----------
        data : dict
            The customer identification data.

        Returns
        -------
        list of dict
            A list of reviews made by the customer.
        """
        customer_username = data.get('customer_username')
        customer_email = data.get('customer_email')

        customer = self.get_customer(customer_username, customer_email)
        reviews = Review.query.filter_by(customer_id=customer.id).all()
        return [review.to_dict() for review in reviews]

    def get_item_reviews(self, data):
        """
        Fetches all reviews for a specific item.

        Parameters
        ----------
        data : dict
            The item identification data.

        Returns
        -------
        list of dict
            A list of reviews for the item.
        """
        item_name = data.get('item_name')
        item_id = data.get('item_id')
        item = self.get_item(item_id, item_name)
        reviews = Review.query.filter_by(item_id=item.id).all()
        return [review.to_dict() for review in reviews]

    @staticmethod
    def get_all_reviews():
        """
        Fetches all reviews in the system.

        Returns
        -------
        list of dict
            A list of all reviews.
        """
        return [review.to_dict() for review in Review.query.all()]
