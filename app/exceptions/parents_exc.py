from http import HTTPStatus


class InvalidCpfLenghtError(Exception):
    message = {"Error": "Check if cpf has 11 characters"}
    status = HTTPStatus.BAD_REQUEST



class InvalidPhoneFormatError(Exception):
    message = {
        "Error": "The phone number is not valid",
        "expected": "(xx) xxxxx-xxxx Parentheses, hyphen and 11 numbers are required.",
    }
    status = HTTPStatus.BAD_REQUEST
