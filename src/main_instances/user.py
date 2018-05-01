class User:
    """
    This is simple user class, that have only it's fields. But initializing it
    you must be sure that your data is RIGHT and CLEAR (i.e validated)
    """
    def __init__(self,
                 uid,
                 login,
                 password,
                 time_zone,
                 nickname,
                 about):
        self._own_tasks = []
        self._projects = []
        self._uid = uid
        self._login = login
        self._nickname = nickname
        self._password = password
        self._time_zone = time_zone
        self._about = about

    def say_hi(self):
        print('hello, I\'m {}'.format(self._nickname))
