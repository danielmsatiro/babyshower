from http import HTTPStatus


class InvalidTypeNumberError(Exception):
    def __init__(self, key) -> None:
        self.message = {"Error": f"The value of keys '{key}' needs to be number!"}
        self.status = HTTPStatus.UNPROCESSABLE_ENTITY
