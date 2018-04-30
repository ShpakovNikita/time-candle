from enum import Enum


# Login related things
class InvalidLoginError(Exception):
    def __init__(self, errors=None, message='The login is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class LoginMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    USER_EXISTS = 'Current user is already exists.'
    USER_NOT_EXISTS = 'Current user is not exists.'
    # TODO: ALREADY_LOGGED_IN


# Password related things
class InvalidPasswordError(Exception):
    def __init__(self, errors=None, message='The password is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class PasswordMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    PASSWORD_IS_NOT_MATCH = 'Typed password is wrong for selected user.'


class InvalidMailError(Exception):
    def __init__(self, message='The mail is invalid! {}', errors=None):
        super().__init__(message.format(errors))
        self.errors = errors
