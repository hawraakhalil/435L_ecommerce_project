from flask import jsonify
from shared.models.CustomersModel import Customer
from sales.src.extensions import jwt

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    customer_id = int(jwt_payload['sub'])
    customer = Customer.query.filter(Customer.id == customer_id).first()
    if customer and customer.last_logout and customer.status == 'active':
        return jwt_payload['iat'] < customer.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
