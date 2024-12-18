from flask import jsonify
from customers.src.extensions import db, jwt
from customers.src.api.v1.customers_service import CustomerService

@jwt.token_in_blocklist_loader
def is_token_revoked(jwt_header, jwt_payload):
    customer_username = jwt_payload['sub']
    customer_service = CustomerService(db.session)
    customer = customer_service.get_customer_by_username(customer_username)
    if customer and customer.last_logout and not customer_service.is_banned and customer.status == 'active':
        return jwt_payload['iat'] < customer.last_logout.timestamp()
    return False

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({'message': 'Token has been revoked'}), 401
