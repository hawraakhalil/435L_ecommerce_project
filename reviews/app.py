from flask import Flask, jsonify
from shared.db import db, migrate
from shared.logger import logger
from reviews.extensions import jwt, cors
from reviews.config import get_config

def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())
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
