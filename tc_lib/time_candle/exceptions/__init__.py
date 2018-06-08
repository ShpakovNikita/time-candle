"""This is the primary exceptions for the whole project. Every module in the
application uses this exceptions for more organized project structure.
"""
from enum import Enum


class AppException(Exception):
    def __init__(self,
                 errors=None,
                 message='Some error occured during the lib interraction! {}'):
        super().__init__(message.format(errors))
        self.errors = errors
        self.message = message


# Login related things
class ConfigError(AppException):
    def __init__(self, errors=None, message='The config is invalid! {}'):
        super().__init__(errors, message)


class ConfigMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    LOG_CONF_INVALID = 'Invalid logger config file or path to it'
