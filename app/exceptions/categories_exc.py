from http import HTTPStatus


class InvalidCategoryError(Exception):
    def __init__(self, invalid_options):
        self.message = {
            "error": "Categories is invalid",
            "invalid_options": list(invalid_options),
            "valid_options": "api/categories",
        }
        self.status = HTTPStatus.UNPROCESSABLE_ENTITY
