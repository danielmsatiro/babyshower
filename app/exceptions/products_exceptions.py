from werkzeug.exceptions import BadRequest


class InvalidDataError(BadRequest):
    ...