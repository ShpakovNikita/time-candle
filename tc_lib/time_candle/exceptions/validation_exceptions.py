from enum import Enum
from . import AppException


# Name related things
class InvalidNameError(AppException):
    def __init__(self, errors=None, message='The typed name is invalid! {}'):
        super().__init__(errors, message)


class NameMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_LOGIN = 'Please retype your login.'
    INVALID_NICKNAME = 'Please retype your nickname.'


# Mail related things
class InvalidMailError(AppException):
    def __init__(self, errors=None, message='The typed mail is invalid! {}'):
        super().__init__(errors, message)


class MailMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_MAIL = 'Please retype your mail.'


# Password related things
class InvalidPasswordError(AppException):
    def __init__(self, errors=None, message='The typed name is invalid! {}'):
        super().__init__(errors, message)


class PasswordMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_PASSWORD = 'Please retype your password. Make sure that it minimum ' \
                       'eight characters, at least one letter and one number'


class InvalidCommentError(AppException):
    def __init__(self, errors=None, message='The typed comment is invalid! {}'):
        super().__init__(errors, message)


class CommentMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_COMMENT = 'Your comment is too long!'


class InvalidTitleError(AppException):
    def __init__(self, errors=None, message='The typed title is invalid! {}'):
        super().__init__(errors, message)


class TitleMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_TITLE = 'Your title is too long!'


# Status related things
class InvalidStatusError(AppException):
    def __init__(self, errors=None, message='The typed status is invalid! {}'):
        super().__init__(errors, message)


class StatusMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_STATUS = 'Please retype status.'


# Priority related things
class InvalidPriorityError(AppException):
    def __init__(
            self, errors=None, message='The typed priority is invalid! {}'):
        super().__init__(errors, message)


class PriorityMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_PRIORITY = 'Please retype priority.'
