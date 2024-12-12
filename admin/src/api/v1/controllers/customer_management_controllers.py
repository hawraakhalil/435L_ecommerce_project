from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from shared.db import db
from admin.src.api.v1.schemas.customer_management_schema import UpdateCustomerProfileSchema, TopUpCustomerSchema, ReverseTransactionSchema, CustomerSchema
from admin.src.api.v1.services.customer_management_service import CustomerManagementService


customer_management_bp = Blueprint('customer_management', __name__, url_prefix='/admin/customers')


@customer_management_bp.route('/top_up_customer', methods=['PUT'])
@jwt_required()
def top_up_customer():
    data = request.get_json()
    schema = TopUpCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.top_up_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    
@customer_management_bp.route('/update_customer_profile', methods=['PUT'])
@jwt_required()
def update_customer_profile():
    data = request.get_json()
    schema = UpdateCustomerProfileSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.update_customer_profile(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/reverse_transaction', methods=['PUT'])
@jwt_required()
def reverse_transaction():
    data = request.get_json()
    schema = ReverseTransactionSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.reverse_transaction(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/get_customer_info', methods=['GET'])
@jwt_required()
def get_customer_info():
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_info(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/get_customer_transactions', methods=['GET'])
@jwt_required()
def get_customer_transactions():
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_transactions(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/ban_customer', methods=['PUT'])
@jwt_required()
def ban_customer():
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.ban_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
    
@customer_management_bp.route('/unban_customer', methods=['PUT'])
@jwt_required()
def unban_customer():
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.unban_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/get_banned_customers', methods=['GET'])
@jwt_required()
def get_banned_customers():
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_all_banned_customers()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@customer_management_bp.route('/get_all_customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_all_customers()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500
