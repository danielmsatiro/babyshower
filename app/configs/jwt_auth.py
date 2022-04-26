from flask_jwt_extended import JWTManager
import os


def init_app(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    JWTManager(app)