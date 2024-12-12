from flask import Flask, jsonify
from inventory.src.api.v1.inventory_controllers import inventory_bp
from inventory.src.extensions import db, migrate, jwt, cors
from inventory.src.utils.logger import logger
from inventory.src.config import get_config


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(inventory_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Inventory API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
