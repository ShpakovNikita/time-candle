class InvalidLoginException(Exception):
    def __init__(self, error_arguments=None):
        self.errorArguments = error_arguments
        Exception.__init__(self, "The login is invalid!")
