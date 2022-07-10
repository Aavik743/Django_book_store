class CustomBaseException(Exception):
    def __init__(self, message, code):
        self.Error = message
        self.Code = code


class BookAlreadyExists(CustomBaseException):
    pass


class NullField(CustomBaseException):
    pass


class NotSuperUser(CustomBaseException):
    pass


class TokenRequired(CustomBaseException):
    pass


class UserDoesNotExist(CustomBaseException):
    pass


class BookDoesNotExist(CustomBaseException):
    pass


class FieldError(CustomBaseException):
    pass


class BookQuantityExceeding(CustomBaseException):
    pass


class CartDoesNotExist(CustomBaseException):
    pass
