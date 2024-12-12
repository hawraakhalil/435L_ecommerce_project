import os
from datetime import timedelta
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.FLASK_ENV = os.getenv('FLASK_ENV')
        if self.FLASK_ENV == 'development':
            self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
        else:
            self.SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_TEST', 'sqlite:///:memory:')
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
        self.JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1800)))
        self.JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 86400)))

def get_config():
    return Config()
