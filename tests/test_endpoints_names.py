def test_route_get_exists(app_get_routes):
    assert app_get_routes.match(
        "/api/products"
    ), 'Verify if exist a route "/api/products available to GET"'
