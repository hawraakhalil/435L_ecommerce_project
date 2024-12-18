from flask import jsonify
from src.extensions import jwt
from src.model.AdminsModel import Admin


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    admin_username = jwt_payload['sub']
    admin = Admin.query.filter(Admin.username == admin_username).first()
    if admin and admin.last_logout:
        return jwt_payload['iat'] < admin.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
