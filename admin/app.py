from flask import Flask, jsonify
from shared.db import db
from shared.logger import logger
from admin.src.api.v1.admin_controllers import admin_bp
from admin.extensions import migrate, jwt, cors
from admin.config import get_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(admin_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Hello, World!'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
