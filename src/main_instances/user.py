import sql_shell.requests
import sql_shell.exceptions
from helper_entities.settings import Settings


class User:
    def __init__(self, uid, login, preferences):
        self._own_tasks = []
        self._projects = []
        self._uid = uid
        self._login = login
        self._preferences = preferences

    @classmethod
    def create_user(cls, login, password):
        """
        If the user already exists in the database, then initialize it with the
        values in it, in other case we will create a new user with no settings.
        :param login: the login of our user
        :param password: password of our user
        :type login: basestring
        :type password: basestring
        :return:
        """

        # TODO: check if the user in database and init it from it

        # This is a dictionary of our user's fields or None if the user is not
        # in the database
        field_dict = sql_shell.requests.find_user(login)

        # The code lower is wrong code, need for changes according to the
        # function's doc declaration

        # uid = sql_shell.requests.get_last_id() + 1
        if field_dict is None:
            raise sql_shell.exceptions.InvalidLoginException()

        preferences = Settings(field_dict['preferences']['password'],
                               None, None, None, None)
        obj = cls(field_dict['uid'], login, preferences)
        return obj

    def say_hi(self):
        print("Hello, I'm {} and my id is {}".format(self._login, self._uid))

    @property
    def login(self):
        return self._login

    @property
    def password(self):
        return self._preferences.password
