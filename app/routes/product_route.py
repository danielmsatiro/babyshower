from app.controllers.product_controller import get_all, get_by_id, get_by_parent, get_by_params
from flask import Blueprint

bp = Blueprint('bp_products', __name__, url_prefix='/products')

bp.get('')(get_all)
bp.get('/params')(get_by_params)
bp.get('/<int:product_id>')(get_by_id)
bp.get('/by_parent/<int:parent_id>')(get_by_parent)