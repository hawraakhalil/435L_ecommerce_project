from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from marshmallow import ValidationError
from werkzeug.exceptions import NotFound

from inventory.extensions import db
from inventory.src.api.v1.inventory_service import InventoryService
from inventory.src.api.v1.inventory_schema import AddItemSchema, RestockItemSchema, UpdateItemSchema, ItemSchema, CategorySchema


inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')


@inventory_bp.route('/add_item', methods=['POST'])
@jwt_required()
def add_item():
    data = request.get_json()
    schema = AddItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in add item: {e.messages}'}), 400
    
    service = InventoryService(db_session=db.session)
    try:
        result = service.add_item(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@inventory_bp.route('/restock_item', methods=['POST'])
@jwt_required()
def restock_item():
    data = request.get_json()
    schema = RestockItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in restock item: {e.messages}'}), 400
    
    service = InventoryService(db_session=db.session)
    try:
        result = service.restock_item(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/update_item', methods=['PUT'])
@jwt_required()
def update_item():
    data = request.get_json()
    schema = UpdateItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in update item: {e.messages}'}), 400
    
    service = InventoryService(db_session=db.session)
    try:
        result = service.update_item(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/delete_item', methods=['DELETE'])
@jwt_required()
def delete_item():
    data = request.get_json()
    schema = ItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in delete item: {e.messages}'}), 400
    
    service = InventoryService(db_session=db.session)
    try:
        result = service.delete_item(data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/get_item', methods=['POST'])
@jwt_required()
def get_item():
    data = request.get_json()
    schema = ItemSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in get item: {e.messages}'}), 400

    item_id = data.get('item_id')
    name = data.get('name')
    service = InventoryService(db_session=db.session)
    try:
        result = service.get_item(item_id, name)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@inventory_bp.route('/get_items', methods=['GET'])
@jwt_required()
def get_items():
    try:
        result = InventoryService.get_items()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/get_items_by_category', methods=['POST'])
@jwt_required()
def get_items_by_category():
    data = request.get_json()
    schema = CategorySchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in get items by category: {e.messages}'}), 400
    
    service = InventoryService(db_session=db.session)

    try:
        result = service.get_items_by_category(data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
