from werkzeug.exceptions import BadRequest


class InvalidDataError(BadRequest):
    ...

class NonexistentProductError(Exception):
    def __init__(self):
        self.message = {
            "error": "Product not found."
        }

        super().__init__(self.message)

class NonexistentParentProductsError(Exception):
    def __init__(self):
        self.message = {
            "error": "No products found for this parent."
        }

        super().__init__(self.message)