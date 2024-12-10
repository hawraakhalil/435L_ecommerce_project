from flask import Flask, jsonify
from src.extensions import db, migrate, jwt, swagger
from src.logger import logger

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    swagger.init_app(app)
    return app

app = create_app()

@app.route('/')
def index():
    logger.info('Enter index')
    return jsonify({'message': 'Hello, World!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
