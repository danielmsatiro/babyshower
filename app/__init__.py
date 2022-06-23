from os import getenv

from flask import Flask
from flask_cors import CORS

from app import commands, routes
from app.configs import database, jwt_auth, migration


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    
    app_url = getenv("APP_URL")

    cors = CORS(
        app,
        resources={
            r"/api*": {
                "origins": f"{app_url}",
            },
        },
        allow_headers=[
            "Authorization",
            "Content-Type",
            "Access-Control-Allow-Credentials",
        ],
        supports_credentials=True,
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    jwt_auth.init_app(app)
    commands.init_app(app)
    routes.init_app(app)

    return app
