def test_route_get_exists(app_get_routes):
    assert app_get_routes.match(
        "/api/products"
    ), 'Verify if there is a route "/api/products available to GET"'
    assert app_get_routes.match(
        f"/api/products/1"
    ), 'Verify if there is a route "/api/products/<product_id> available to GET"'
    assert app_get_routes.match(
        f"/api/products/by_parent/1"
    ), 'Verify if there is a route "/api/products/by_parent/<parent_id> available to GET"'
    assert app_get_routes.match(
        f"/api/categories"
    ), 'Verify if there is a route "/api/category> available to GET"'
    assert app_get_routes.match(
        f"/api/parents"
    ), 'Verify if there is a route "/api/parents> available to GET"'
    assert app_get_routes.match(
        f"/api/questions/by_product/1"
    ), 'Verify if there is a route "/api/questions/by_product/<product_id> available to GET"'
    """ assert app_get_routes.match(
        f"/api/answers/by_question/1"
    ), 'Verify if there is a route "/api/answers/by_product/<question_id> available to GET"' """


""" def test_route_post_exists(app_post_routes):
    assert app_post_routes.match(
        f"/api/products"
    ), 'Verify if there is a route "/api/products available to POST"'
    assert app_post_routes.match(
        f"/api/parents"
    ), 'Verify if there is a route "/api/parents available to POST"'
    assert app_post_routes.match(
        f"/api/asks/1"
    ), 'Verify if there is a route "/api/asks<product_id> available to POST"'
    assert app_post_routes.match(
        f"/api/answers/1"
    ), 'Verify if there is a route "/api/answers<ask_id> available to POST"'


def test_route_patch_exists(app_patch_routes):
    assert app_patch_routes.match(
        f"/api/products/1"
    ), 'Verify if there is a route "/api/products/<product_id> available to PATCH"'
    assert app_patch_routes.match(
        f"/api/parents/1"
    ), 'Verify if there is a route "/api/parents/<parent_id> available to PATCH"'
    assert app_patch_routes.match(
        f"/api/asks/1"
    ), 'Verify if there is a route "/api/asks/<ask_id> available to PATCH"'
    assert app_patch_routes.match(
        f"/api/answers/1"
    ), 'Verify if there is a route "/api/answers/<answer_id> available to PATCH"'


def test_route_delete_exists(app_delete_routes):
    assert app_delete_routes.match(
        f"/api/products/1"
    ), 'Verify if there is a route "/api/products/<product_id> available to PATCH"'
    assert app_delete_routes.match(
        f"/api/parents/1"
    ), 'Verify if there is a route "/api/parents/<parent_id> available to PATCH"'
    assert app_delete_routes.match(
        f"/api/asks/1"
    ), 'Verify if there is a route "/api/asks/<ask_id> available to PATCH"'
    assert app_delete_routes.match(
        f"/api/answers/1"
    ), 'Verify if there is a route "/api/answers/<answer_id> available to PATCH"' """
