from flask import Flask, jsonify
from shared.db import db, migrate
from shared.logger import logger
from admin.src.api.v1.controllers.admin_controllers import admin_bp
from admin.src.api.v1.services.customer_management_service import customer_management_service
from admin.src.extensions import jwt, cors
from admin.src.config import get_config
from admin.src.token_management import is_token_revoked, revoked_token_callback

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(admin_bp)
    app.register_blueprint(customer_management_service)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Admin API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
