from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, BadRequest

from src.extensions import db
from src.utils.logger import logger

from src.api.v1.sales_schema import PurchaseSchema, ReversePurchaseSchema, ItemSchema
from src.api.v1.sales_service import SalesService
from src.utils.errors import InsufficientStock, InsufficientBalance


sales_bp = Blueprint('sales', __name__, url_prefix='/sales')


@sales_bp.route('/purchase', methods=['PUT'])
@jwt_required()
def purchase():
    logger.info('Enter purchase')
    data = request.get_json()
    schema = PurchaseSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in purchase: {e.messages}')
        return jsonify({'error': f'Validation error in purchase: {e.messages}'}), 400

    customer_username = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.purchase(data, customer_username)
        logger.info('Exit purchase successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except InsufficientStock as e:
        return jsonify({'error': str(e)}), 409
    except InsufficientBalance as e:
        return jsonify({'error': str(e)}), 410
    except Exception as e:
        logger.info(f'Internal server error in purchase: {e}')
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/reverse_purchase', methods=['PUT'])
@jwt_required()
def reverse_purchase():
    logger.info('Enter reverse purchase')
    data = request.get_json()
    schema = ReversePurchaseSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in reverse purchase: {e.messages}')
        return jsonify({'error': f'Validation error in reverse purchase: {e.messages}'}), 400

    customer_username = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.reverse_purchase(data, customer_username)
        logger.info('Exit reverse purchase successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 408
    except Exception as e:
        logger.info(f'Internal server error in reverse purchase: {e}')
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/get_customer_transactions', methods=['GET'])
@jwt_required()
def get_customer_transactions():
    logger.info('Enter get customer transactions')
    customer_username = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.get_customer_transactions(customer_username)
        logger.info('Exit get customer transactions successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.info(f'Internal server error in get customer transactions: {e}')
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/inquire_item', methods=['POST'])
@jwt_required()
def inquire_item():
    logger.info('Enter inquire item')
    data = request.get_json()
    schema = ItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        logger.info(f'Validation error in inquire item: {e.messages}')
        return jsonify({'error': f'Validation error in inquire item: {e.messages}'}), 400

    service = SalesService(db_session=db.session)
    try:
        result = service.inquire_item(data)
        logger.info('Exit inquire item successfully')
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/get_all_items', methods=['GET'])
@jwt_required()
def get_all_items():
    logger.info('Enter get all items')
    service = SalesService(db_session=db.session)
    try:
        result = service.get_all_items()
        logger.info('Exit get all items successfully')
        return jsonify(result), 200
    except Exception as e:
        logger.info(f'Internal server error in get all items: {e}')
        return jsonify({'error': str(e)}), 500
