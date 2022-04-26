from flask.testing import FlaskClient

#POST
def test_create_question(client: FlaskClient):
    payload = {
        "question": "teste"
    }
    response = client.post("/api/questions/1", json=payload)
    expected = {
        "id": 1,
        "question": "teste",
        "product_id": 1,
        "parent_id": 1
    }

    assert (
        response.status_code == 201
    ), "Check your status code at route 'post questions/<product_id>'"
    assert (
        response.json == expected
    ), "Check your body request at route 'post questions/<product_id>'"

#GET
def test_get_question(client: FlaskClient):
    response = client.get("/api/question/1")
    expected = [
            {"id": 1, "question": "teste", "product_id": 1, "parent_id": 1}
        ]

    assert (
        response.status_code == 200
    ), "Check your status code at route 'get questions/<product_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'get questions/<product_id>'"

#PATCH
def test_patch_question(client: FlaskClient):
    payload = {
        "question": "teste atualizado"
    }
    response = client.patch("api/questions/1", json=payload)
    expected = {
        "id": 1,
        "question": "teste atualizado",
        "product_id": 1,
        "parent_id": 1
    }
    
    assert (
        response.status_code == 201
    ), "Check your status code at route 'patch questions/<question_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'patch questions/<product_id>'"

#DELETE 
def test_delete_question(client: FlaskClient):
    response = client.delete("api/questions/1")
    expected = {"msg": "Question deleted"}

    assert (
        response.status_code == 200
    ), "Check your status code at route 'patch questions/<question_id>'"
    assert (
        response.json == expected
    ), "Something went wrong at route 'patch questions/<product_id>'"



