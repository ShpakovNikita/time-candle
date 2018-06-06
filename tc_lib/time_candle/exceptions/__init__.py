"""This is the primary exceptions for the whole project. Every module in the
application uses this exceptions for more organized project structure.
"""
from enum import Enum


def custom_excepthook(exc_type, exc_value, tb):
    # Exception type and value
    print(' %s: %s' % (exc_type.__name__, exc_value))


# Login related things
class ConfigError(Exception):
    def __init__(self, errors=None, message='The config is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class ConfigMessages(Enum):
    # This is pre defined messages that will be associated with user all over
    # the project
    LOG_CONF_INVALID = 'Invalid logger config file or path to it'
