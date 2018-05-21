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
    def __init__(self, errors=None, message='The mail is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


# Task related things
class InvalidTidError(Exception):
    def __init__(self, errors=None, message='The tid is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class TaskMessages(Enum):
    # This is pre defined messages that will be associated with task all over
    # the project
    TASK_DOES_NOT_EXISTS = 'Selected task does not exists'


# Project related things
class InvalidPidError(Exception):
    def __init__(self, errors=None, message='The pid is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class ProjectMessages(Enum):
    # This is pre defined messages that will be associated with projects all
    # over the project
    PROJECT_DOES_NOT_EXISTS = 'Selected project does not exists'
    DO_NOT_HAVE_RIGHTS = 'You don\'t have rights to modify this project'
    USER_ALREADY_EXISTS = 'The selected user already exists in this project'


# Filters related things
class InvalidFilterOperator(Exception):
    def __init__(self, errors=None, message='The filter operator is invalid! {}'
                 ):
        super().__init__(message.format(errors))
        self.errors = errors


class InvalidFilter(Exception):
    def __init__(self, errors=None, message='The filter is invalid! {}'
                 ):
        super().__init__(message.format(errors))
        self.errors = errors


class FilterMessages(Enum):
    # This is pre defined messages that will be associated with filters all
    # over the project
    FILTER_DOES_NOT_EXISTS = 'Selected operator is invalid'
    FILTER_ITEMS_NOT_EXISTS = 'Selected filter items do not exists'