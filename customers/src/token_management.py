from flask import jsonify
from shared.db import db
from customers.src.extensions import jwt
from customers.src.api.v1.customers_service import CustomerService

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    customer_id = int(jwt_payload['sub'])
    customer_service = CustomerService(db.session)
    customer = customer_service.get_customer_by_id(customer_id)
    if customer and customer.last_logout and not customer_service.is_customer_banned(customer_id) and customer.status == 'active':
        return jwt_payload['iat'] < customer.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401