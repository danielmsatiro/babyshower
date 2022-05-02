from flask.testing import FlaskClient


def create_answer_test(client: FlaskClient):
    status_code = 201

    body_data = {"answer": "No céu tem pão?", "mother": 1, "question_id": 2}

    body_data_keys = body_data.keys()

    response = {"id": 1, "answer": "No céu tem pão?", "mother": 1, "question_id": 2}

    response_data_keys = response.keys()

    body_valid_keys = ["answer", "mother_id", "question_id"]

    response_valid_keys = ["id", "answer", "mother_id", "question_id"]

    assert status_code == 201, "Verificando se o statuscode retornado é 201 - CREATED"

    assert (
        body_valid_keys.sort() == body_data_keys.sort()
    ), "Verificando as chaves do corpo da requisição"

    assert (
        response_valid_keys.sort() == response_data_keys.sort()
    ), "Verificando as chaves da resposta"
