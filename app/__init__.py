from os import getenv

from flask import Flask

from app import routes
from app.configs import commands, database, migration


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DB_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    commands.init_app(app)

    routes.init_app(app)

    return app
