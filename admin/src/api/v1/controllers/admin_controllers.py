from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from werkzeug.exceptions import NotFound
from marshmallow import ValidationError
from admin.src.errors import AuthenticationError

from shared.db import db
from admin.src.api.v1.schemas.admin_schema import RegisterAdminSchema, LoginAdminSchema, UpdateAdminSchema
from admin.src.api.v1.services.admin_service import AdminService


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/register_admin', methods=['PUT'])
def register_admin():
    data = request.get_json()
    schema = RegisterAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in register admin: {e.messages}'}), 400
    
    service = AdminService(db_session =db.session)
    try:
        result = service.register_admin(data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@admin_bp.route('/login_admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    schema = LoginAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in login admin: {e.messages}'}), 400
    
    service = AdminService(db_session=db.session)
    try:
        result = service.login_admin(data)
        return jsonify(result), 200
    except AuthenticationError as e:
        return jsonify({'error': str(e)}), 403
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/logout_admin', methods=['DELETE'])
@jwt_required()
def logout_admin():
    admin_id = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.logout_admin(admin_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/update_admin', methods=['PUT'])
@jwt_required()
def update_admin():
    data = request.get_json()
    schema = UpdateAdminSchema()
    try:
        data = schema.load(data)
    except ValidationError as e:
        return jsonify({'error': f'Validation error in update customer: {e.messages}'}), 400
    
    admin_id = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.update_admin(admin_id, data)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/get_admin_info', methods=['POST'])
@jwt_required()
def get_admin_info():
    admin_id = get_jwt_identity()
    service = AdminService(db_session=db.session)
    try:
        result = service.get_admin_info(admin_id)
        return jsonify(result), 200
    except NotFound as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

