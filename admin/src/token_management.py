from flask import jsonify
from admin.src.extensions import jwt
from shared.db import db
from admin.src.api.v1.services.admin_service import AdminService

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    admin_id = jwt_payload['sub']
    admin_service = AdminService(db.session)
    admin = admin_service.get_admin_by_id(admin_id)
    if admin.last_logout:
        return jwt_payload['iat'] < admin.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
