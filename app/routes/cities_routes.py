from app.controllers import cities_controller
from flask import Blueprint

bp = Blueprint("cities", __name__, url_prefix="/cities")

bp.get("")(cities_controller.retrieve)
