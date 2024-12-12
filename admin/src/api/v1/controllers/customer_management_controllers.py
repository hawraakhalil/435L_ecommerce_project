from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, Forbidden
from marshmallow import ValidationError

from shared.db import db
from admin.src.api.v1.schemas.customer_management_schema import (
    UpdateCustomerProfileSchema,
    TopUpBalanceSchema,
    ReverseTransactionSchema
)
from admin.src.api.v1.services.customer_management_service import CustomerManagementService
from admin.src.api.v1.services.admin_service import AdminService

customer_management_bp = Blueprint('customer_management', __name__, url_prefix='/admin/customers')

@customer_management_bp.before_request
@jwt_required()
def verify_admin():
    admin_id = get_jwt_identity()
    admin_service = AdminService(db_session=db.session)
    try:
        admin_service.get_admin_by_id(admin_id)
    except NotFound:
        return jsonify({'error': 'Unauthorized access. Admin privileges required.'}), 403

@customer_management_bp.route('/update_customer_profile/<int:customer_id>', methods=['PUT'])
def update_customer_profile(customer_id):
    data = request.get_json()
    schema = UpdateCustomerProfileSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.update_customer_profile(customer_id, data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/top_up_balance/<int:customer_id>', methods=['PUT'])
def top_up_balance(customer_id):
    data = request.get_json()
    schema = TopUpBalanceSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.top_up_balance(customer_id, data['amount'])
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/reverse_transaction', methods=['PUT'])
def reverse_transaction():
    data = request.get_json()
    schema = ReverseTransactionSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error: {e.messages}'}), 400
    
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.reverse_transaction(data['transaction_id'])
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/get_customer_info/<int:customer_id>', methods=['GET'])
def get_customer_info(customer_id):
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_info(customer_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/get_customer_transactions/<int:customer_id>', methods=['GET'])
def get_customer_transactions(customer_id):
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_transactions(customer_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/get_all_customers', methods=['GET'])
def get_all_customers():
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_all_customers()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/block_customer/<int:customer_id>', methods=['PUT'])
def block_customer(customer_id):
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.block_customer(customer_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customer_management_bp.route('/unblock_customer/<int:customer_id>', methods=['PUT'])
def unblock_customer(customer_id):
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.unblock_customer(customer_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
