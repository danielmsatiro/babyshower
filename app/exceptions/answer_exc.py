from http import HTTPStatus


class NotAuthorizedError(Exception):
    message = {"Error": "User not authorized"}
    status = HTTPStatus.BAD_REQUEST
