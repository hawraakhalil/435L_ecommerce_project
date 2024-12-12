from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from shared.db import db
from reviews.src.api.v1.reviews_service import ReviewsService
from reviews.src.api.v1.reviews_schema import AddReviewSchema, UpdateReviewSchema, ReviewSchema, GetCustomerReviewsSchema, ReviewSchema


reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')


@reviews_bp.route('/add_review', methods=['PUT'])
@jwt_required()
def add_review():
    data = request.get_json()
    schema = AddReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in add review: {e.messages}'}), 400
    
    customer_id = get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.add_review(data, customer_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/update_review', methods=['PUT'])
@jwt_required()
def update_review():
    data = request.get_json()
    schema = UpdateReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in update review: {e.messages}'}), 400
    
    customer_id = get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.update_review(data, customer_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/delete_review', methods=['DELETE'])
@jwt_required()
def delete_review():
    data = request.get_json()
    schema = ReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in delete review: {e.messages}'}), 400
    
    customer_id = get_jwt_identity()
    service = ReviewsService(db_session=db.session)
    try:
        result = service.delete_review(data, customer_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_customer_reviews', methods=['POST'])
@jwt_required()
def get_customer_reviews():
    data = request.get_json()
    schema = GetCustomerReviewsSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in get customer reviews: {e.messages}'}), 400
    
    service = ReviewsService(db_session=db.session)
    try:
        result = service.get_customer_reviews(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_item_reviews', methods=['POST'])
@jwt_required()
def get_item_reviews():
    data = request.get_json()
    schema = ReviewSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in get item reviews: {e.messages}'}), 400
    
    service = ReviewsService(db_session=db.session)
    try:
        result = service.get_item_reviews(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reviews_bp.route('/get_all_reviews', methods=['GET'])
@jwt_required()
def get_all_reviews():
    try:
        result = ReviewsService.get_all_reviews()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

