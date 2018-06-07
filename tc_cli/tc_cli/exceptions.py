from enum import Enum


# Base exception
class AuthenticationError(Exception):
    def __init__(self, errors=None, message='The authentication failed {}'):
        super().__init__(message.format(errors))
        self.errors = errors


# Login related things
class InvalidLoginError(AuthenticationError):
    def __init__(self, errors=None, message='The login is invalid! {}'):
        super().__init__(errors, message)


class LoginMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    USER_EXISTS = 'Current user is already exists.'
    USER_DOES_NOT_EXISTS = 'Current user is not exists.'
    ALREADY_LOGGED_IN = 'Already logged in'
    NO_USER_TO_DELETE = 'There is no such user to delete'
    ADMIN_CANNOT_REMOVE_HIMSELF = 'You are an admin of this project, you' \
                                  ' cannot be removed'


# Uid related things
class InvalidUidError(AuthenticationError):
    def __init__(self, errors=None, message='The uid is invalid! {}'):
        super().__init__(errors, message)


# Password related things
class InvalidPasswordError(AuthenticationError):
    def __init__(self, errors=None, message='The password is invalid! {}'):
        super().__init__(errors, message)


class PasswordMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    PASSWORD_IS_NOT_MATCH = 'Typed password is wrong for selected user.'
