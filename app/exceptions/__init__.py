from http import HTTPStatus


class InvalidKeyError(Exception):
    def __init__(self, received_key, expected_key):
        self.message = {
            "expected_keys": list(expected_key),
            "wrong_keys": list(received_key),
        }
        self.status = HTTPStatus.UNPROCESSABLE_ENTITY


class InvalidTypeValueError(Exception):
    message = {"Error": "Check if type is a string"}
    status = HTTPStatus.UNAUTHORIZED


class NotFoundError(Exception):
    def __init__(self, id, modelclass):
        self.message = {"Error": f"{modelclass}: id {id} not found"}
        self.status = HTTPStatus.NOT_FOUND
