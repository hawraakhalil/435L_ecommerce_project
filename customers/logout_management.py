from flask import jsonify
from src.extensions import db, jwt
from src.api.v1.services.customers_service import CustomerService

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    customer_id = jwt_payload['sub']
    customer_service = CustomerService(db.session)
    customer = customer_service.get_customer_by_id(customer_id)
    if customer.last_logout:
        return jwt_payload['iat'] < customer.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401