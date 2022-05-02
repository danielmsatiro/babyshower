from app.controllers import chat_controller
from flask import Blueprint

bp = Blueprint("bp_chat", __name__, url_prefix="/chat")


bp.get("/other_parent_id")(chat_controller.get_chat)
bp.post("/other_parent_id")(chat_controller.post_message)
