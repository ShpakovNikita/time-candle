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
    USER_DOES_NOT_EXISTS = 'Current user is not exists.'
    ALREADY_LOGGED_IN = 'Already logged in'
    NO_USER_TO_DELETE = 'There is no such user to delete'
