from http import HTTPStatus


class UserOrChatNotFoundError(Exception):
    message = {"details": "You do not have chat with this user or user not found"}
    status = HTTPStatus.NOT_FOUND