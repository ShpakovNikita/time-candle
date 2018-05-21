class InvalidLoginException(Exception):
    def __init__(self, error_arguments=None):
        self.errorArguments = error_arguments
        Exception.__init__(self, "The login is invalid!")


# Validators exceptions
class InvalidArgumentFormat(Exception):
    def __init__(self, errors=None, message='The argument is invalid! {}'):
        super().__init__(message.format(errors))
        self.errors = errors
