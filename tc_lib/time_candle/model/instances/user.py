from time_candle.model import logger


class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """

    def __init__(self,
                 uid=None,
                 login='guest',
                 nickname='guest',
                 about=''):
        self.uid = uid
        self.login = login
        self.nickname = nickname
        self.about = about

    @classmethod
    def make_user(cls, obj):
        """
        This function converts some data type to user
        :type obj: type with fields:
        - uid
        - login
        - nickname
        - about
        :return: User
        """
        logger.debug('convert storage to model user')

        user = cls(uid=obj.uid,
                   login=obj.login,
                   nickname=obj.nickname,
                   about=obj.about)

        return user
