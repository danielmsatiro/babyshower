from app.controllers import categories_controller
from flask import Blueprint

bp_categories = Blueprint('categories', __name__, url_prefix='/categories')

bp_categories.get('')(categories_controller.retrieve)