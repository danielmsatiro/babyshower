from app.routes.route_test import bp as bp_products
from app.routes.parents_routes_test import bp as bp_parents
from flask import Blueprint, Flask

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask) -> None:
    bp_api.register_blueprint(bp_products)
    bp_api.register_blueprint(bp_parents)
    app.register_blueprint(bp_api)
