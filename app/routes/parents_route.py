from app.controllers import parents_controller
from flask import Blueprint

bp = Blueprint("bp_parents", __name__, url_prefix="/parents")


def test_get_parents():
    ...


bp.get("")(parents_controller.pick_parents)
bp.get("/<int:parent_id>")(parents_controller.pick_parents_by_id)
bp.post("")(parents_controller.new_parents)
bp.post("/login")(parents_controller.login)
bp.patch("")(parents_controller.update_parents)
bp.delete("")(parents_controller.delete_parents)
