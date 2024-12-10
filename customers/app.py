from flask import Flask
from .src.api.v1.customers_controllers import customer_bp
from extensions import jwt

def create_app():
    app = Flask(__name__)
    app.register_blueprint(customer_bp, url_prefix="/customers")
    jwt.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
    
from flask import Flask
from flask_migrate import Migrate
from shared.db import db
from shared.models import *  # Import all models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://username:password@db_host:5432/ecommerce_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(port=5001)
