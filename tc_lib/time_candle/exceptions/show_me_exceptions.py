from enum import Enum
from time_candle.exceptions import AppException


# few elements in commend
class FewElementsError(AppException):
    def __init__(self, errors=None, message='Too few elements in command! {}'):
        super().__init__(errors, message)


# invalid expression
class InvalidExpressionError(AppException):
    def __init__(self, errors=None, message='Too few elements in command! {}'):
        super().__init__(errors, message)


class ShowMeMessages(Enum):
    NO_ELEMENTS_FOR_FILTER = 'Specify the elements for selected command'
    UNEXPECTED_SYMBOL_FOUND = 'Make sure that your request is right'
    UNEXPECTED_LITERAL_TYPE = 'Please input correct literal of type or None'
    NOT_LEGAL_OPERATOR_SEQUENCE = 'Make sure that you typed operators correctly'
    INVALID_TEMPLATE_USAGE = 'Make sure that you typed your template params ' \
                             'correctly'
