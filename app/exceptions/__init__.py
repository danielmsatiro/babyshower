from http import HTTPStatus


class InvalidKeyError(Exception):
    def __init__(self, received_key, expected_key):
        self.message = {
            "expected_keys": list(expected_key),
            "received_keys": list(received_key),
        }
        self.status = HTTPStatus.UNPROCESSABLE_ENTITY


class InvalidTypeValueError(Exception):
    def __init__(self, key) -> None:
        self.message = {"Error": f"The value of keys '{key}' needs to be string!"}
        self.status = HTTPStatus.UNPROCESSABLE_ENTITY


class NotFoundError(Exception):
    def __init__(self, id, modelclass):
        self.message = {"Error": f"{modelclass}: id {id} not found"}
        self.status = HTTPStatus.NOT_FOUND


class NotAuthorizedError(Exception):
    message = {"Error": "User not authorized"}
    status = HTTPStatus.UNAUTHORIZED
