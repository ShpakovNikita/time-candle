from enum import Enum


# Name related things
class InvalidNameError(Exception):
    def __init__(self, errors=None, message='The typed name is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class NameMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_LOGIN = 'Please retype your login.'
    INVALID_NICKNAME = 'Please retype your nickname.'


# Mail related things
class InvalidMailError(Exception):
    def __init__(self, errors=None, message='The typed mail is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class MailMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_MAIL = 'Please retype your mail.'


# Password related things
class InvalidPasswordError(Exception):
    def __init__(self, errors=None, message='The typed name is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class PasswordMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    INVALID_PASSWORD = 'Please retype your password. Make sure that it minimum ' \
                       'eight characters, at least one letter and one number'
