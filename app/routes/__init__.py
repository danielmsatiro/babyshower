from app.routes.route_test import bp as bp_products
from flask import Blueprint, Flask

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask) -> None:
    bp_api.register_blueprint(bp_products)

    app.register_blueprint(bp_api)
