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


class InvalidEmailError(Exception):
    message = {"Error": "Email is not valid"}
    status = HTTPStatus.BAD_REQUEST
    

class NonexistentParentError(Exception):
    def __init__(self):
        self.message = {"error": "Parent not found."}

        super().__init__(self.message)    

class NotIsLoggedParentError(Exception):
    message = {"Error": "Not is logged user"}
    status = HTTPStatus.BAD_REQUEST