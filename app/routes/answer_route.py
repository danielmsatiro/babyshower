from app.controllers.answers_controller import (
    create_answer,
    delete_answer,
    read_answer,
    update_answer,
)
from flask import Blueprint

bp = Blueprint("bp_answers", __name__, url_prefix="answers")

bp.post("/by_question/<int:question_id>")(create_answer)
bp.get("/<int:answer_id>")(read_answer)
bp.patch("/<int:answer_id>")(update_answer)
bp.delete("/<int:answer_id>")(delete_answer)
