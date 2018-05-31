"""This is the primary exceptions for the whole project. Every module in the
application uses this exceptions for more organized project structure.

"""


def custom_excepthook(exc_type, exc_value, tb):
    # Exception type and value
    print(' %s: %s' % (exc_type.__name__, exc_value))
