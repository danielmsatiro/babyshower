from flask import Blueprint

bp = Blueprint("bp_products", __name__, url_prefix="/products")


def function_test():
    ...


bp.get("")(function_test)
