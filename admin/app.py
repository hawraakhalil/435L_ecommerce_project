from flask import Flask, jsonify
from admin.src.utils.logger import logger
from admin.src.extensions import db, migrate, jwt, cors
from admin.src.config import get_config

from admin.src.model.AdminsModel import Admin
from admin.src.model.CustomersModel import Customer
from admin.src.model.TransactionsModel import Transaction

from admin.src.api.v1.controllers.admin_controllers import admin_bp
from admin.src.api.v1.controllers.customer_management_controllers import customer_management_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_management_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Admin API'}), 200

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)