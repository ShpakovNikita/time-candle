from enum import Enum


# few elements in commend
class FewElementsError(Exception):
    def __init__(self, errors=None, message='Too few elements in command! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


# invalid expression
class InvalidExpressionError(Exception):
    def __init__(self, errors=None, message='Too few elements in command! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class ShowMeMessages(Enum):
    NO_ELEMENTS_FOR_FILTER = 'Spicify the elements for selected command'
    UNEXPECTED_SYMBOL_FOUND = 'Make sure that your request is right'
