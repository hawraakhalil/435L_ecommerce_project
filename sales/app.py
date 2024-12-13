import os
import sys

# Dynamically add the project's base directory to PYTHONPATH
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Get the absolute path to the directory containing app.py
sys.path.append(BASE_DIR)  # Add this directory to sys.path

from flask import Flask, jsonify
from src.utils.logger import logger
from src.api.v1.sales_controllers import sales_bp
from src.extensions import db, migrate, jwt, cors
from src.config import get_config
from src.token_management import is_token_revoked, revoked_token_callback


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(sales_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Sales API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
