from http import HTTPStatus


class NotAuthorizedError(Exception):
    message = {"Error": "Unauthorized access"}
    status = HTTPStatus.UNAUTHORIZED


class InvalidKeyError(Exception):
    message = {"Error": "Check if key name is question"}
    status = HTTPStatus.UNAUTHORIZED


class InvalidTypeValueError(Exception):
    message = {"Error": "Check if type is a string"}
    status = HTTPStatus.UNAUTHORIZED
