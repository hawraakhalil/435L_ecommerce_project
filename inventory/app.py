from flask import Flask, jsonify
from inventory.extensions import migrate, cors  
from shared.logger import logger
from shared.db import db
from inventory.src.api.v1.inventory_controllers import inventory_bp
from admin.extensions import jwt


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Hello, World!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
