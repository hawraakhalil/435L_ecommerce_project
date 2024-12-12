from flask import Flask, jsonify
from customers.src.extensions import db, migrate, jwt, cors
from customers.src.utils.logger import logger
from customers.src.config import get_config
from customers.src.token_management import is_token_revoked, revoked_token_callback

from customers.src.model.CustomersModel import Customer

from customers.src.api.v1.customers_controllers import customers_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(customers_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Customers API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
