from app.routes.product_route import bp as bp_products
from app.routes.categories_route import bp as bp_categories

from flask import Blueprint, Flask


bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask) -> None:
    bp_api.register_blueprint(bp_products)
    bp_api.register_blueprint(bp_categories)

    app.register_blueprint(bp_api)
