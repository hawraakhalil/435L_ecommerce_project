"""
customers.routes
================

This module defines the API routes for customer-related operations.

Blueprint
---------
customers_bp : Flask Blueprint
    The blueprint for handling customer-related routes.

Routes
------
- `/register_customer` : Register a new customer.
- `/login_customer` : Log in a customer.
- `/logout_customer` : Log out a customer.
- `/update_customer` : Update customer information.
- `/get_customer_info` : Retrieve customer details.
"""

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from customers.src.extensions import db
from customers.src.utils.logger import logger
from customers.src.utils.errors import AuthenticationError

from customers.src.api.v1.customers_schema import (
    RegisterCustomerSchema,
    LoginCustomerSchema,
    UpdateCustomerSchema,
)
from customers.src.api.v1.customers_service import CustomerService

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')


@customers_bp.route('/register_customer', methods=['PUT'])
def register_customer():
    """
    Registers a new customer.

    This endpoint handles the registration of a new customer by validating
    input data and invoking the CustomerService to create a new record.

    Returns
    -------
    Response
        JSON response indicating success or error with appropriate HTTP status.
    """
    logger.info('Enter register customer')
    data = request.get_json()
    schema = RegisterCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in register customer: {e.messages}')
        return jsonify({'error': f'Validation error in register customer: {e.messages}'}), 400

    service = CustomerService(db_session=db.session)
    try:
        result = service.register_customer(data)
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f'Internal server error in register customer: {e}')
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/login_customer', methods=['POST'])
def login_customer():
    """
    Logs in a customer.

    This endpoint validates the provided login credentials and generates
    a JWT token upon successful authentication.

    Returns
    -------
    Response
        JSON response with the token or error message.
    """
    logger.info('Enter login customer')
    data = request.get_json()
    schema = LoginCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in login customer: {e.messages}')
        return jsonify({'error': f'Validation error in login customer: {e.messages}'}), 400

    service = CustomerService(db_session=db.session)
    try:
        result = service.login_customer(data)
        logger.info('Exit login customer successfully')
        return jsonify(result), 200
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 403
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in login customer: {e}')
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/logout_customer', methods=['DELETE'])
@jwt_required()
def logout_customer():
    """
    Logs out the currently authenticated customer.

    Returns
    -------
    Response
        JSON response indicating success or error.
    """
    logger.info('Enter logout customer')
    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.logout_customer(customer_username)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in logout customer: {e}')
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/update_customer', methods=['PUT'])
@jwt_required()
def update_customer():
    """
    Updates the details of the currently authenticated customer.

    Returns
    -------
    Response
        JSON response indicating success or error with updated customer details.
    """
    logger.info('Enter update customer')
    data = request.get_json()
    schema = UpdateCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in update customer: {e.messages}')
        return jsonify({'error': f'Validation error in update customer: {e.messages}'}), 400

    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.update_customer(customer_username, data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in update customer: {e}')
        return jsonify({'error': str(e)}), 500


@customers_bp.route('/get_customer_info', methods=['POST'])
@jwt_required()
def get_customer_info():
    """
    Retrieves information about the currently authenticated customer.

    Returns
    -------
    Response
        JSON response with the customer's details or error message.
    """
    logger.info('Enter get customer info')
    customer_username = get_jwt_identity()
    service = CustomerService(db_session=db.session)
    try:
        result = service.get_customer_info(customer_username)
        logger.info('Exit get customer info successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in get customer info: {e}')
        return jsonify({'error': str(e)}), 500
