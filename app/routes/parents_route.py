from app.controllers import parents_controller
from flask import Blueprint

bp = Blueprint("bp_parents", __name__, url_prefix="/parents")

def test_get_parents():
    ...

bp.get('')(parents_controller.pick_parents)
bp.post('')(parents_controller.new_parents)
bp.patch('/<int:product_cpf>')(parents_controller.update_parents)
bp.delete('/<int:product_id>')(parents_controller.delete_parents)