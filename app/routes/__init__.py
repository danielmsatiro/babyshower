from app.routes.product_route import bp as bp_products
from app.routes.categories_route import bp as bp_categories
from app.routes.question_route import bp as bp_questions
from app.routes.parents_route import bp as bp_parents
from app.routes.answer_route import bp as bp_answers

from flask import Blueprint, Flask


bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


def init_app(app: Flask) -> None:
    bp_api.register_blueprint(bp_products)
    bp_api.register_blueprint(bp_categories)
    bp_api.register_blueprint(bp_questions)
    bp_api.register_blueprint(bp_parents)
    bp_api.register_blueprint(bp_answers)
    app.register_blueprint(bp_api)
