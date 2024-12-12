from flask import jsonify
from inventory.src.extensions import jwt
from shared.models import Admin


@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    admin_id = jwt_payload['sub']
    admin = Admin.query.filter(Admin.id == admin_id).first()
    if admin.last_logout:
        return jwt_payload['iat'] < admin.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
