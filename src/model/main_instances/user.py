from model import logger


class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """

    def __init__(self,
                 uid_=None,
                 login_='guest',
                 password_=None,
                 time_zone_=None,
                 nickname_='guest',
                 about_=''):
        self.own_tasks = []
        self.projects = []
        self.uid = uid_
        self.login = login_
        self.nickname = nickname_
        self.password = password_
        self.time_zone = time_zone_
        self.about = about_

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
        :return: User
        """
        logger.debug('convert storage to model user')

        user = cls(obj.uid,
                   obj.login,
                   obj.password,
                   obj.time_zone,
                   obj.nickname,
                   obj.about)

        return user
