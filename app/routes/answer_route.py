from flask import Blueprint

from app.controllers.answers_controller import (
    create_answer,
    read_answer,
    update_answer,
    delete_answer,
)


bp = Blueprint("answers", __name__, url_prefix="answers")

bp.post("/<int:question_id>")(create_answer)
bp.get("/<int:answer_id>")(read_answer)
bp.patch("/<int:answer_id>")(update_answer)
bp.delete("/<int:answer_id>")(delete_answer)
