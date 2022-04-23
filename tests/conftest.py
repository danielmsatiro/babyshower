from flask import Flask
from pytest import fail, fixture


@fixture
def app():
    try:
        return __import__("app").create_app()
    except ModuleNotFoundError:
        fail('Verify if the file "app.py" exists')
    except AttributeError:
        fail('Vefify if the variable "app" exists')


@fixture
def cliente(app: Flask):
    with app.test_client() as client:
        return client


@fixture
def app_get_routes(app: Flask):
    return app.url_map.bind("", default_method="GET")


@fixture
def app_post_routes(app: Flask):
    return app.url_map.bind("", default_method="POST")


@fixture
def app_patch_routes(app: Flask):
    return app.url_map.bind("", default_method="PATCH")


@fixture
def app_delete_routes(app: Flask):
    return app.url_map.bind("", default_method="DELETE")
