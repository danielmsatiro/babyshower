from flask import Blueprint

bp = Blueprint("bp_parents", __name__, url_prefix="/parents")

def test_get_parents():
    ...

bp.get("")(test_get_parents)