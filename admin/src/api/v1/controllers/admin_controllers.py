"""
admin.routes
============

This module defines the API routes for admin-related operations.

Blueprint
---------
admin_bp : Flask Blueprint
    The blueprint for handling admin-related routes.

Routes
------
- `/register_admin` : Register a new admin.
- `/login_admin` : Log in an admin.
- `/logout_admin` : Log out an admin.
- `/update_admin` : Update admin information.
- `/get_admin_info` : Retrieve admin details.
"""

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.exceptions import NotFound, BadRequest
from marshmallow import ValidationError

from admin.src.utils.errors import AuthenticationError
from admin.src.utils.logger import logger
from admin.src.extensions import db
from admin.src.api.v1.schemas.admin_schema import RegisterAdminSchema, LoginAdminSchema, UpdateAdminSchema
from admin.src.api.v1.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/register_admin', methods=['PUT'])
def register_admin():
    """
    Registers a new admin.

    This endpoint validates the provided data and creates a new admin record in the database.

    Returns
    -------
    Response
        JSON response indicating success or validation errors with the appropriate HTTP status.
    """
    logger.info('Enter register admin')
    data = request.get_json()
    schema = RegisterAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.error(f'Validation error in register admin: {e.messages}')
        return jsonify({'error': f'Validation error in register admin: {e.messages}'}), 400

    service = AdminService(db_session=db.session)
    try:
        result = service.register_admin(data)
        logger.info('Exit register admin successfully')
        return jsonify(result), 201
    except BadRequest as e:
        return jsonify({'error': str(e)}), 408
    except Exception as e:
        logger.error(f'Internal server error in register admin: {e}')
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/login_admin', methods=['POST'])
def login_admin():
    """
    Logs in an admin.

    This endpoint authenticates an admin using the provided credentials.

    Returns
    -------
    Response
        JSON response containing access and refresh tokens or error messages.
    """
    logger.info('Enter login admin')
    data = request.get_json()
    schema = LoginAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.error(f'Validation error in login admin: {e.messages}')
        return jsonify({'error': f'Validation error in login admin: {e.messages}'}), 400

    service = AdminService(db_session=db.session)
    try:
        result = service.login_admin(data)
        logger.info('Exit login admin successfully')
        return jsonify(result), 200
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 401
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in login admin: {e}')
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/logout_admin', methods=['DELETE'])
@jwt_required()
def logout_admin():
    """
    Logs out the currently authenticated admin.

    Returns
    -------
    Response
        JSON response indicating success or error with the appropriate HTTP status.
    """
    logger.info('Enter logout admin')
    admin_username = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.logout_admin(admin_username)
        logger.info('Exit logout admin successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in logout admin: {e}')
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/update_admin', methods=['PUT'])
@jwt_required()
def update_admin():
    """
    Updates the details of the currently authenticated admin.

    This endpoint validates the provided data and updates the admin record in the database.

    Returns
    -------
    Response
        JSON response indicating success or validation errors with the appropriate HTTP status.
    """
    logger.info('Enter update admin')
    data = request.get_json()
    schema = UpdateAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.error(f'Validation error in update admin: {e.messages}')
        return jsonify({'error': f'Validation error in update admin: {e.messages}'}), 400

    admin_username = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.update_admin(admin_username, data)
        logger.info('Exit update admin successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in update admin: {e}')
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/get_admin_info', methods=['GET'])
@jwt_required()
def get_admin_info():
    """
    Retrieves information about the currently authenticated admin.

    Returns
    -------
    Response
        JSON response containing admin details or an error message.
    """
    logger.info('Enter get admin info')
    admin_username = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.get_admin_info(admin_username)
        logger.info('Exit get admin info successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f'Internal server error in get admin info: {e}')
        return jsonify({'error': str(e)}), 500
