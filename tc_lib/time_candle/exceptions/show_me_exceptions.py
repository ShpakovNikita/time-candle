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
    NO_ELEMENTS_FOR_FILTER = 'Specify the elements for selected command'
    UNEXPECTED_SYMBOL_FOUND = 'Make sure that your request is right'
    UNEXPECTED_LITERAL_TYPE = 'Please input correct literal of type or None'
    NOT_LEGAL_OPERATOR_SEQUENCE = 'Make sure that you typed operators correctly'
