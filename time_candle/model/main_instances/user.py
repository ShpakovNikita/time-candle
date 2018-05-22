from model import logger


class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """

    def __init__(self,
                 uid=None,
                 login='guest',
                 password=None,
                 time_zone=None,
                 nickname='guest',
                 about='',
                 mail=None):
        self.own_tasks = []
        self.projects = []
        self.uid = uid
        self.login = login
        self.nickname = nickname
        self.password = password
        self.time_zone = None
        self.about = about
        self.mail = mail

    @classmethod
    def make_user(cls, obj):
        """
        This function converts some data type to user
        :type obj: type with fields:
        - uid
        - login
        - password
        - time_zone
        - nickname
        - about
        - mail
        :return: User
        """
        logger.debug('convert storage to model user')

        user = cls(uid=obj.uid,
                   login=obj.login,
                   password=obj.password,
                   nickname=obj.nickname,
                   about=obj.about,
                   mail=obj.mail)

        return user
