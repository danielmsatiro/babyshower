from app.controllers import chat_controller
from flask import Blueprint

bp = Blueprint("bp_chat", __name__, url_prefix="/chat")

bp.get("/<int:other_parent_id>")(chat_controller.read_chat)
bp.post("/<int:other_parent_id>")(chat_controller.post_message)
