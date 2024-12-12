from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from reviews.src.extensions import db
from reviews.src.utils.logger import logger

from reviews.src.api.v1.reviews_service import ReviewsService
from reviews.src.api.v1.reviews_schema import AddReviewSchema, UpdateReviewSchema, GetCustomerReviewsSchema, ReviewSchema


reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('/add_review', methods=['PUT'])
@jwt_required()
def add_review():
    logger.info('Enter add review')
    data = request.get_json()
    schema = AddReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in add review: {e.messages}')
        return jsonify({'error': f'Validation error in add review: {e.messages}'}), 400
    
    customer_username= get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.add_review(data, customer_username)
        logger.info('Exit add review successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in add review: {e}')
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/update_review', methods=['PUT'])
@jwt_required()
def update_review():
    logger.info('Enter update review')
    data = request.get_json()
    schema = UpdateReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in update review: {e.messages}')
        return jsonify({'error': f'Validation error in update review: {e.messages}'}), 400
    
    customer_username = get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.update_review(data, customer_username)
        logger.info('Exit update review successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in update review: {e}')
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/delete_review', methods=['DELETE'])
@jwt_required()
def delete_review():
    logger.info('Enter delete review')
    data = request.get_json()
    schema = ReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in delete review: {e.messages}')
        return jsonify({'error': f'Validation error in delete review: {e.messages}'}), 400
    
    customer_username = get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.delete_review(data, customer_username)
        logger.info('Exit delete review successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in delete review: {e}')
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_customer_reviews', methods=['POST'])
@jwt_required()
def get_customer_reviews():
    logger.info('Enter get customer reviews')
    data = request.get_json()
    schema = GetCustomerReviewsSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in get customer reviews: {e.messages}')
        return jsonify({'error': f'Validation error in get customer reviews: {e.messages}'}), 400
    
    service = ReviewsService(db_session=db.session)
    try:
        result = service.get_customer_reviews(data)
        logger.info('Exit get customer reviews successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in get customer reviews: {e}')
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_item_reviews', methods=['POST'])
@jwt_required()
def get_item_reviews():
    logger.info('Enter get item reviews')
    data = request.get_json()
    schema = ReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in get item reviews: {e.messages}')
        return jsonify({'error': f'Validation error in get item reviews: {e.messages}'}), 400
    
    service = ReviewsService(db_session=db.session)
    try:
        result = service.get_item_reviews(data)
        logger.info('Exit get item reviews successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in get item reviews: {e}')
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_all_reviews', methods=['GET'])
@jwt_required()
def get_all_reviews():
    logger.info('Enter get all reviews')
    try:
        result = ReviewsService.get_all_reviews()
        logger.info('Exit get all reviews successfully')
        return jsonify(result), 200
    except Exception as e:
        logger.info(f'Internal server error in get all reviews: {e}')
        return jsonify({'error': str(e)}), 500
