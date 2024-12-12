from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from customers.src.extensions import db
from customers.src.utils.logger import logger
from customers.src.utils.errors import AuthenticationError


from customers.src.api.v1.customers_schema import RegisterCustomerSchema, LoginCustomerSchema, UpdateCustomerSchema
from customers.src.api.v1.customers_service import CustomerService


customers_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customers_bp.route('/register_customer', methods=['PUT'])
def register_customer():
    data = request.get_json()
    schema = RegisterCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in register customer: {e.messages}'}), 400
    
    service = CustomerService(db_session =db.session)
    try:
        result = service.register_customer(data)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@customers_bp.route('/login_customer', methods=['POST'])
def login_customer():
    data = request.get_json()
    schema = LoginCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in login customer: {e.messages}'}), 400
    
    service = CustomerService(db_session=db.session)
    try:
        result = service.login_customer(data)
        return jsonify(result), 200
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 403
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/logout_customer', methods=['DELETE'])
@jwt_required()
def logout_customer():
    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.logout_customer(customer_username)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/update_customer', methods=['PUT'])
@jwt_required()
def update_customer():
    data = request.get_json()
    schema = UpdateCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in update customer: {e.messages}'}), 400
    
    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.update_customer(customer_username, data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers_bp.route('/get_customer_info', methods=['POST'])
@jwt_required()
def get_customer_info():
    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.get_customer_info(customer_username)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
