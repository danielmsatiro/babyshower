from app.controllers import question_controller
from flask import Blueprint

bp = Blueprint("bp_questions", __name__, url_prefix="/questions")

bp.get("/by_product/<int:product_id>")(
    question_controller.get_product_questions)
bp.post("/by_product/<int:product_id>")(question_controller.create_question)
bp.patch("/<int:question_id>")(question_controller.update_question)
bp.delete("/<int:question_id>")(question_controller.delete_question)
