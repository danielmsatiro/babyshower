""" from flask.testing import FlaskClient


def test_without_query_params(client: FlaskClient):
    response = client.get("/api/products")

    assert {
        response.status_code == 200
    }, "Verifique se está retornando 200 quando bem sucedido na rota GET /products"
    assert response.json == {
        {"id": 1, "name": "sabonete", "price": 5.99},
    }, "Verifique se a mensagem de sucesso de GET /products está formatada corretamente" """
