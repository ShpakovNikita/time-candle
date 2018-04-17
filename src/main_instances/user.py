import sql_shell.requests as r
import sql_shell.exceptions


class User:
    def __init__(self, uid, login, preferences):
        self._own_tasks = []
        self._projects = []
        self._uid = uid
        self._login = login
        self._preferences = preferences

    @classmethod
    def new_user(cls, login):
        uid = r.get_last_id() + 1
        if r.find_name(login) is None:
            raise sql_shell.exceptions.InvalidLoginException()

        obj = cls(uid, login, None)
        return obj

    def say_hi(self):
        print("Hello, I'm {} and my id is {}".format(self._login, self._uid))
