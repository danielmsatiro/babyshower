from http import HTTPStatus


class DataAlreadyExists(Exception):
    ...


class InvalidTypeValueError(Exception):
    message = {"Error": "Check if your values type is a string"}
    status = HTTPStatus.UNAUTHORIZED


class InvalidEmailLenghtError(Exception):
    message = {"Error": "Check if cpf has 11 characters"}
    status = HTTPStatus.UNAUTHORIZED


class InvalidPhoneFormatError(Exception):
    message = {
        "Error": "The phone number is not valid",
        "expected": "(xx) xxxxx-xxxx Parentheses, hyphen and 11 numbers are required.",
    }
    status = HTTPStatus.UNAUTHORIZED
