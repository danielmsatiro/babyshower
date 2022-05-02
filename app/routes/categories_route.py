from app.controllers import categories_controller
from flask import Blueprint

bp = Blueprint("bp_categories", __name__, url_prefix="/categories")

bp.get("")(categories_controller.retrieve)
