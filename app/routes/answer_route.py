from flask import Blueprint

from app.controllers.answers_controller import (
    create_answer,
    read_answer,
    update_answer,
    delete_answer
)


bp = Blueprint('answers', __name__, url_prefix='answers')

bp.post('/<int:id>')(create_answer)
bp.get('/<int:id>')(read_answer)
bp.patch('/<int:id>')(update_answer)
bp.delete('/<int:id>')(delete_answer)
