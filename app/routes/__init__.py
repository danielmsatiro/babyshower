from app.routes.answer_route import bp as bp_answers
from app.routes.categories_route import bp as bp_categories
from app.routes.chat_route import bp as bp_chat
from app.routes.cities_routes import bp as bp_cities
from app.routes.parents_route import bp as bp_parents
from app.routes.product_route import bp as bp_products
from app.routes.question_route import bp as bp_questions
from flask import Blueprint, Flask, render_template

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")


@bp_api.get("")
def home():
    return render_template("readme.html")


def init_app(app: Flask) -> None:
    bp_api.register_blueprint(bp_products)
    bp_api.register_blueprint(bp_categories)
    bp_api.register_blueprint(bp_questions)
    bp_api.register_blueprint(bp_parents)
    bp_api.register_blueprint(bp_answers)
    bp_api.register_blueprint(bp_chat)
    bp_api.register_blueprint(bp_cities)
    app.register_blueprint(bp_api)
