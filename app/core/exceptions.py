class UserError(Exception):
    pass


class InvalidUserInput(UserError):
    pass


class EmailAlreadyExists(UserError):
    pass

class UserNotFound(UserError):
    pass

class AppException(Exception):
    def __init__(self, code: str, message: str, details: dict | None = None):
        self.code = code
        self.message = message
        self.details = details
