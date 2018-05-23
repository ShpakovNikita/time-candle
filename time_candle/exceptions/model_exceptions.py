from enum import Enum


class InvalidLoginException(Exception):
    def __init__(self, error_arguments=None):
        self.errorArguments = error_arguments
        Exception.__init__(self, "The login is invalid!")


# Validators exceptions
class InvalidArgumentFormat(Exception):
    def __init__(self, errors=None, message='The argument is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


# Password related things
class InvalidTimeError(Exception):
    def __init__(self, errors=None, message='The time is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors


class TimeMessages(Enum):
    # This is pre defined messages that will be associated with password all
    # over the project
    TIME_STAMP = 'You cannot create tasks in the past'
