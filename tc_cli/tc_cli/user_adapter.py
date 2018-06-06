from peewee import *
import time_candle.exceptions.db_exceptions as db_e
from time_candle.module_app import logger
import os

db_filename = 'users.db'
_db_proxy = Proxy()


class User(Model):
    uid = PrimaryKeyField()

    # user fields
    # for UserModel's own_tasks we have a relation field in Task class from
    # storage.task_adapter

    # projects [] -> see the UserProjectRelation table
    login = CharField(unique=True)

    # settings field
    password = CharField()
    mail = CharField(null=True)
    nickname = CharField(default='')

    # time_zone will be saved in the form of shift in milliseconds
    # time_zone = IntegerField(default=0)
    about = CharField(default='')

    class Meta:
        database = _db_proxy


# Constants that show our operators
OP_AND = 0
OP_OR = 1


class UserFilter:
    def __init__(self):
        self.result = []
        self.ops = []

    @staticmethod
    def _union_filter():
        return None

    # clear filter query
    def clear(self):
        self.result = []
        self.ops = []

    # make groups operation
    def __and__(self, other):
        fil = UserFilter()
        fil.ops.append(OP_AND)
        fil.result.append(self.to_query())
        fil.result.append(other.to_query())
        return fil

    def __or__(self, other):
        fil = UserFilter()
        fil.ops.append(OP_OR)
        fil.result.append(self.to_query())
        fil.result.append(other.to_query())
        return fil

    # Generate query to make result array to the peewee object
    def to_query(self):
        query = None
        if not self.result:
            return self._union_filter()

        # try to get result's first element
        try:
            query = self.result[0]
        except IndexError:
            pass

        for i in range(len(self.result) - 1):
            if self.ops[i] == OP_AND:
                query = query & self.result[i + 1]

            elif self.ops[i] == OP_OR:
                query = query | self.result[i + 1]

            else:
                raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                                 FILTER_DOES_NOT_EXISTS)

        return query

    def uid(self, uid, op=OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.uid == uid)
        return self

    def login_substring(self, substring, op=OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(substring))
        return self

    def login_regex(self, regex, op=OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(regex))
        return self

    def nickname_substring(self, substring, op=OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(substring))
        return self

    def nickname_regex(self, regex, op=OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(regex))
        return self


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
    def get_by_filter(filter_instance):
        """
        This function returns storage objects by the given UserFilter.
        :param filter_instance: UserFilter with defined filters
        :return: List of User objects without passwords
        """
        query = User.select().where(filter_instance.to_query())

        # this is we need in case of password flipping, just fot security
        def _init_usr(self, obj):
            self.uid = obj.uid
            self.login = obj.login
            self.time_zone = None
            self.nickname = obj.nickname
            self.about = obj.about
            self.mail = obj.mail

        user_dummie = type('user_dummie', (), {'__init__': _init_usr,
                                               'password': None})

        result = []
        for user in query:
            result.append(user_dummie(user))

        return result

    @staticmethod
    def login_user(login, password):
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
            raise db_e.InvalidLoginError(
                str(db_e.LoginMessages.USER_DOES_NOT_EXISTS) +
                ', try to login again')

        if obj.password != password:
            raise db_e.InvalidPasswordError(
                db_e.PasswordMessages.PASSWORD_IS_NOT_MATCH)

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
         - login,
         - password
         - nickname,
         - about,
         - mail
        :return: None
        """
        if User.select().where(User.login == obj.login).exists():
            raise db_e.InvalidLoginError(db_e.LoginMessages.USER_EXISTS)

        User.create(login=obj.login,
                    password=obj.password,
                    about=obj.about,
                    nickname=obj.nickname,
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
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    @staticmethod
    def get_user_by_id(uid):
        """
        This function returns login of user by id
        :param uid: User's id
        :return: String
        """
        query = User.select().where(User.uid == uid)
        try:
            # user instance
            obj = query.get()

        except DoesNotExist:
            raise db_e.InvalidUidError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

        return obj
