from app.controllers import product_controller
from flask import Blueprint

bp = Blueprint('bp_products', __name__, url_prefix='/products')

bp.post('')(product_controller.create_product)
bp.get('')(product_controller.get_all)
bp.get('/params')(product_controller.get_by_params)
bp.get('/<int:product_id>')(product_controller.get_by_id)
bp.get('/by_parent/<int:parent_id>')(product_controller.get_by_parent)
bp.patch('/<int:product_id>')(product_controller.update_product)
bp.delete('/<int:product_id>')(product_controller.delete_product)