from peewee import *
import tc_cli.exceptions as auth_e
from tc_cli import logger
import os

db_filename = 'users.db'
_db_proxy = Proxy()


class User(Model):
    uid = PrimaryKeyField()
    login = CharField(unique=True)

    # settings field
    password = CharField()
    mail = CharField(null=True)

    class Meta:
        database = _db_proxy


class UserAdapter:

    _db_initialized = False

    def __init__(self, db_name=db_filename, uid=None):
        self.uid = uid

        if db_name is None:
            db_name = db_filename

        self.db_name = db_name
        self._db_exists = os.path.exists(self.db_name)

        if not self._db_initialized:
            self._db_initialize()
            self._db_initialized = True

        if not self._db_exists:
            self._create_database()

            # but this will never be used later
            self._db_exists = True

    @staticmethod
    def _create_database():
        User.create_table()
        logger.debug("Database created")

    def _db_initialize(self):
        db = SqliteDatabase(self.db_name)
        _db_proxy.initialize(db)

    # TODO: rm?
    def _db_exists(self):
        return os.path.exists(self.db_name)

    @staticmethod
    def authenticate(login, password):
        """
        This function is like head function for all adapters. From this start
        point we get real user from database by it's login and valid password
        :param login: login of searching user
        :param password: password of searching user
        :type login: String
        :type password: String
        :return: User
        """
        query = User.select().where(User.login == login)

        try:
            # user instance
            obj = query.get()

        except DoesNotExist:
            raise auth_e.InvalidLoginError(
                str(auth_e.LoginMessages.USER_DOES_NOT_EXISTS) +
                ', try to login again')

        if obj.password != password:
            raise auth_e.InvalidPasswordError(
                auth_e.PasswordMessages.PASSWORD_IS_NOT_MATCH)

        return obj

    @staticmethod
    def save(obj):
        """
        This function if checking is current user exists, and if so we are
        raising an exception. Or we are adding it to the database.
        This function is used to store given task to the database. Note, that
        tasks can be with similar names and dates (but on that case I have a
        task below)
        :param obj: type with fields:
         - login
         - password
         - mail
        :return: None
        """
        if User.select().where(User.login == obj.login).exists():
            raise auth_e.InvalidLoginError(auth_e.LoginMessages.USER_EXISTS)

        User.create(login=obj.login,
                    password=obj.password,
                    mail=obj.mail)

    @staticmethod
    def get_id_by_login(login):
        """
        This function checks if user by passed login exists in the database and
        returns user's id, or raises an error
        :param login: User's login
        :return: Int
        """
        try:
            return User.select().where(User.login == login).get().uid

        except DoesNotExist:
            raise auth_e.InvalidLoginError(
                auth_e.LoginMessages.USER_DOES_NOT_EXISTS)
