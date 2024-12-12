from flask import Flask, jsonify
from shared.db import db, migrate
from shared.logger import logger
from sales.src.api.v1.sales_controllers import sales_bp
from sales.extensions import jwt, cors
from sales.config import get_config

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
    app.run(host='0.0.0.0', port=5003, debug=True)
