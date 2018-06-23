from enum import Enum
from time_candle.exceptions import AppException


class DatabaseConfigureError(AppException):
    def __init__(self, errors=None,
                 message='The database is not properly configured {}'):
        super().__init__(errors, message)


class DatabaseMessages(Enum):
    # This is pre defined messages that will be associated with db errors all
    # over the project
    MULTIPLE_DATABASE_SELECTION = 'You passed init params for postgres and ' \
                                  'sqlite database'
    INVALID_PSQL_CONFIG = """Make sure that your config has following format:
    {
        'NAME': 'mydb',
        'USER': 'shaft',
        'HOST': '/var/run/postgresql',
        'PASSWORD': '',
        'PORT': '5432'
    }"""


# Login related things
class InvalidLoginError(AppException):
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
class InvalidUidError(AppException):
    def __init__(self, errors=None, message='The uid is invalid! {}'):
        super().__init__(errors, message)


# Password related things
class InvalidPasswordError(AppException):
    def __init__(self, errors=None, message='The password is invalid! {}'):
        super().__init__(errors, message)


class PasswordMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    PASSWORD_IS_NOT_MATCH = 'Typed password is wrong for selected user.'


class InvalidMailError(AppException):
    def __init__(self, errors=None, message='The mail is invalid! {}'):
        super().__init__(errors, message)


# Task related things
class InvalidTidError(AppException):
    def __init__(self, errors=None, message='The tid is invalid! {}'):
        super().__init__(errors, message)


class TaskMessages(Enum):
    # This is pre defined messages that will be associated with task all over
    # the project
    TASK_DOES_NOT_EXISTS = 'Selected task does not exists (at least for you)'
    DO_NOT_HAVE_RIGHTS = 'You don\'t have rights to create/change task here'


# Project related things
class InvalidPidError(AppException):
    def __init__(self, errors=None, message='The pid is invalid! {}'):
        super().__init__(errors, message)


class ProjectMessages(Enum):
    # This is pre defined messages that will be associated with projects all
    # over the project
    PROJECT_DOES_NOT_EXISTS = 'Selected project does not exists'
    DO_NOT_HAVE_RIGHTS = 'You don\'t have rights to modify this project'
    USER_ALREADY_EXISTS = 'The selected user already exists in this project'


# Project related things
class InvalidMidError(AppException):
    def __init__(self, errors=None, message='The pid is invalid! {}'):
        super().__init__(errors, message)


class MidMessages(Enum):
    # This is pre defined messages that will be associated with projects all
    # over the project
    DO_NOT_HAVE_RIGHTS = 'You don\'t have rights to modify this message'


# Filters related things
class InvalidFilterOperator(AppException):
    def __init__(self, errors=None, message='The filter operator is invalid! {}'
                 ):
        super().__init__(errors, message)


class InvalidFilter(AppException):
    def __init__(self, errors=None, message='The filter is invalid! {}'
                 ):
        super().__init__(errors, message)


class FilterMessages(Enum):
    # This is pre defined messages that will be associated with filters all
    # over the project
    FILTER_DOES_NOT_EXISTS = 'Selected operator is invalid'
    FILTER_ITEMS_NOT_EXISTS = 'Selected filter items do not exists'
