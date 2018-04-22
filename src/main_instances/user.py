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
    def create_user(cls, login):
        """
        If the user already exists in the database, then initialize it with the
        values in it, in other case we will create a new user with no settings.
        :param login:
        :return:
        """

        # TODO: check if the user in database and init it from it

        # The code lower is wrong code, need for changes according to the
        # function's doc declaration

        uid = r.get_last_id() + 1
        if r.find_name(login) is None:
            raise sql_shell.exceptions.InvalidLoginException()

        obj = cls(uid, login, None)
        return obj

    def say_hi(self):
        print("Hello, I'm {} and my id is {}".format(self._login, self._uid))

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._preferences.password
