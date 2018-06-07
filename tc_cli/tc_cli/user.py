from . import logger


class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """

    def __init__(self,
                 uid=None,
                 login='guest',
                 password=None,
                 mail=None):
        self.uid = uid
        self.login = login
        self.password = password
        self.mail = mail

    @classmethod
    def make_user(cls, obj):
        """
        This function converts some data type to user
        :type obj: type with fields:
        - uid
        - login
        - password
        - mail
        :return: User
        """
        logger.debug('make user auth model')

        user = cls(uid=obj.uid,
                   password=obj.password,
                   mail=obj.mail)

        return user
