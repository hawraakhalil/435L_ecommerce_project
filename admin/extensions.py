from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
swagger = Swagger(template={
    "swagger": "2.0",
    "info": {
        "title": "Ecomerce Application",
        "description": "A simple ecomerce application",
        "version": "0.0.1",
    },
    "securityDefinitions": {
        "jwt": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your Bearer token in the format **Bearer {token}**"
        }
    }
})
