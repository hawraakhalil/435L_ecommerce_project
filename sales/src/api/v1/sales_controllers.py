from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from marshmallow import ValidationError
from werkzeug.exceptions import NotFound, BadRequest

from shared.db import db
from sales.src.api.v1.sales_schema import PurchaseSchema, ReversePurchaseSchema, ItemSchema
from sales.src.api.v1.sales_service import SalesService
from sales.errors import InsufficientStock, InsufficientBalance


sales_bp = Blueprint('sales', __name__)


@sales_bp.route('/purchase', methods=['PUT'])
@jwt_required()
def purchase():
    data = request.get_json()
    schema = PurchaseSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in purchase: {e.messages}'}), 400

    user_id = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.purchase(data, user_id)
        return jsonify(result), 200
    except InsufficientStock as e:
        return jsonify({'error': str(e)}), 301
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except InsufficientBalance as e:
        return jsonify({'error': str(e)}), 406
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@sales_bp.route('/reverse_purchase', methods=['PUT'])
@jwt_required()
def reverse_purchase():
    data = request.get_json()
    schema = ReversePurchaseSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in reverse purchase: {e.messages}'}), 400

    user_id = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.reverse_purchase(data, user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except BadRequest as e:
        return jsonify({'error': str(e)}), 405
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/get_user_transactions', methods=['POST'])
@jwt_required()
def get_user_transactions():
    user_id = get_jwt_identity()
    service = SalesService(db_session=db.session)
    try:
        result = service.get_user_transactions(user_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/inquire_item', methods=['GET'])
def inquire_item():
    data = request.get_json()
    schema = ItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in inquire item: {e.messages}'}), 400

    service = SalesService(db_session=db.session)
    try:
        result = service.inquire_item(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sales_bp.route('/get_all_items', methods=['GET'])
def get_all_items():
    service = SalesService(db_session=db.session)
    try:
        result = service.get_all_items()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
