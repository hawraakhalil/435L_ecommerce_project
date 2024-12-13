"""
admin.customer_management
=========================

This module defines the API routes for managing customers within the admin panel.

Blueprint
---------
customer_management_bp : Flask Blueprint
    The blueprint for handling customer management-related routes.

Routes
------
- `/top_up_customer` : Top up a customer's balance.
- `/update_customer_profile` : Update a customer's profile.
- `/reverse_transaction` : Reverse a customer's transaction.
- `/get_customer_info` : Retrieve information about a specific customer.
- `/get_customer_transactions` : Retrieve a customer's transactions.
- `/ban_customer` : Ban a customer.
- `/unban_customer` : Unban a customer.
- `/get_banned_customers` : Retrieve all banned customers.
- `/get_all_customers` : Retrieve all customers.
"""

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from admin.src.extensions import db
from admin.src.utils.logger import logger
from admin.src.api.v1.schemas.customer_management_schema import (
    UpdateCustomerProfileSchema,
    TopUpCustomerSchema,
    ReverseTransactionSchema,
    CustomerSchema
)
from admin.src.api.v1.services.customer_management_service import CustomerManagementService

customer_management_bp = Blueprint('customer_management', __name__, url_prefix='/admin/customers')


@customer_management_bp.route('/top_up_customer', methods=['PUT'])
@jwt_required()
def top_up_customer():
    """
    Top up a customer's balance.

    Validates the input data and adds the specified amount to the customer's balance.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter top up customer')
    data = request.get_json()
    schema = TopUpCustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in top up customer: {e.messages}')
        return jsonify({'error': f'Validation error in top up customer: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.top_up_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 408
    except Exception as e:
        logger.error(f'Internal server error in top up customer: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/update_customer_profile', methods=['PUT'])
@jwt_required()
def update_customer_profile():
    """
    Update a customer's profile.

    Validates the input data and updates the specified customer's profile.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter update customer profile')
    data = request.get_json()
    schema = UpdateCustomerProfileSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in update customer profile: {e.messages}')
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.update_customer_profile(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in update customer profile: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/reverse_transaction', methods=['PUT'])
@jwt_required()
def reverse_transaction():
    """
    Reverse a customer's transaction.

    Validates the input data and reverses the specified transaction.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter reverse transaction')
    data = request.get_json()
    schema = ReverseTransactionSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in reverse transaction: {e.messages}')
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
        logger.error(f'Internal server error in reverse transaction: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/get_customer_info', methods=['POST'])
@jwt_required()
def get_customer_info():
    """
    Retrieve information about a specific customer.

    Validates the input data and retrieves the specified customer's details.

    Returns
    -------
    Response
        JSON response containing customer details or an error message.
    """
    logger.info('Enter get customer info')
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in get customer info: {e.messages}')
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_info(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in get customer info: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/get_customer_transactions', methods=['POST'])
@jwt_required()
def get_customer_transactions():
    """
    Retrieve a customer's transactions.

    Validates the input data and retrieves the specified customer's transaction history.

    Returns
    -------
    Response
        JSON response containing the transaction history or an error message.
    """
    logger.info('Enter get customer transactions')
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in get customer transactions: {e.messages}')
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_customer_transactions(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in get customer transactions: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/ban_customer', methods=['PUT'])
@jwt_required()
def ban_customer():
    """
    Ban a customer.

    Validates the input data and bans the specified customer.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter ban customer')
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in ban customer: {e.messages}')
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.ban_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in ban customer: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/unban_customer', methods=['PUT'])
@jwt_required()
def unban_customer():
    """
    Unban a customer.

    Validates the input data and unbans the specified customer.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter unban customer')
    data = request.get_json()
    schema = CustomerSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in unban customer: {e.messages}')
        return jsonify({'error': f'Validation error: {e.messages}'}), 400

    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.unban_customer(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in unban customer: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/get_banned_customers', methods=['GET'])
@jwt_required()
def get_banned_customers():
    """
    Retrieve all banned customers.

    Returns
    -------
    Response
        JSON response containing a list of banned customers or an error message.
    """
    logger.info('Enter get banned customers')
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_all_banned_customers()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Internal server error in get banned customers: {e}')
        return jsonify({'error': str(e)}), 500


@customer_management_bp.route('/get_all_customers', methods=['GET'])
@jwt_required()
def get_all_customers():
    """
    Retrieve all customers.

    Returns
    -------
    Response
        JSON response containing a list of all customers or an error message.
    """
    logger.info('Enter get all customers')
    service = CustomerManagementService(db_session=db.session)
    try:
        result = service.get_all_customers()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Internal server error in get all customers: {e}')
        return jsonify({'error': str(e)}), 500
