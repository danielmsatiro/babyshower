from flask import Blueprint

from app.controllers.answers_controller import create_answer


bp_answer = Blueprint('answers', __name__, url_prefix='answers')

bp_answer.post('/<int:id>')(create_answer)
