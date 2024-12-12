from flask import Flask, jsonify
from shared.db import db, migrate
from shared.logger import logger
from reviews.src.api.v1.reviews_controllers import reviews_bp
from reviews.src.extensions import jwt, cors
from reviews.src.config import get_config
from reviews.src.token_management import is_token_revoked, revoked_token_callback


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    app.register_blueprint(reviews_bp)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Reviews API'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
