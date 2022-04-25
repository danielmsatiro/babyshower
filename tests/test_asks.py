from flask.testing import FlaskClient

#POST
def test_create_ask(client: FlaskClient):
    payload = {
        "question": "teste"
    }
    response = client.post("/api/asks/1", json=payload)
    expected = {
        "id": 1,
        "question": "teste",
        "product_id": 1,
        "parent_id": 1
    }

    assert (
        response.status_code == 201
    ), "Check your status code at route 'post asks/<product_id>'"
    assert (
        response.json == expected
    ), "Check your body request at route 'post asks/<product_id>'"

#GET
def test_get_asks(client: FlaskClient):
    response = client.get("/api/asks/1")
    expected = [
            {"id": 1, "question": "teste", "product_id": 1, "parent_id": 1}
        ]

    assert (
        response.status_code == 200
    ), "Check your status code at route 'get asks/<product_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'get asks/<product_id>'"

#PATCH
def test_patch_ask(client: FlaskClient):
    payload = {
        "question": "teste atualizado"
    }
    response = client.patch("api/asks/1", json=payload)
    expected = {
        "id": 1,
        "question": "teste atualizado",
        "product_id": 1,
        "parent_id": 1
    }
    
    assert (
        response.status_code == 201
    ), "Check your status code at route 'patch asks/<ask_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'patch asks/<product_id>'"

#DELETE 
def test_delete_ask(client: FlaskClient):
    response = client.delete("api/asks/1")
    expected = {"msg": "Question deleted"}

    assert (
        response.status_code == 200
    ), "Check your status code at route 'patch asks/<ask_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'patch asks/<product_id>'"



