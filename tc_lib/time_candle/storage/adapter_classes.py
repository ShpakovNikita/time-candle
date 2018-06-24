from peewee import *
from playhouse import db_url
import time_candle.exceptions.db_exceptions as db_e
import os
from time_candle.storage import logger


db_filename = ':memory:'
_db_proxy = Proxy()


class Filter:
    # Constants that show our operators
    OP_AND = 0
    OP_OR = 1

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
        fil = Filter()
        fil.ops.append(Filter.OP_AND)
        fil.result.append(self.to_query())
        fil.result.append(other.to_query())
        return fil

    def __or__(self, other):
        fil = Filter()
        fil.ops.append(Filter.OP_OR)
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
            if self.ops[i] == Filter.OP_AND:
                query = query & self.result[i + 1]

            elif self.ops[i] == Filter.OP_OR:
                query = query | self.result[i + 1]

            else:
                raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                                 FILTER_DOES_NOT_EXISTS)

        return query


class BaseModel(Model):
    class Meta:
        database = _db_proxy


class User(BaseModel):
    uid = CharField(unique=True)

    # user fields
    # for UserModel's own_tasks we have a relation field in Task class from
    # storage.task_adapter
    login = CharField(unique=True)

    # settings field
    nickname = CharField(default='')
    about = CharField(default='')


class Message(BaseModel):
    mid = PrimaryKeyField()

    content = CharField()

    # user's uid
    uid = CharField()


class Project(BaseModel):
    pid = PrimaryKeyField()

    title = CharField()
    admin = IntegerField()
    description = TextField()


class Task(BaseModel):
    tid = PrimaryKeyField()

    creator = IntegerField()

    # if the task is not project task this field equals to the creator field
    receiver = IntegerField()

    # if the task is not project task this field equals null
    project = ForeignKeyField(Project, related_name='project', null=True)
    status = SmallIntegerField()
    parent = ForeignKeyField('self', null=True)

    title = CharField()
    priority = SmallIntegerField()

    # Time in milliseconds. Nullable for further functionality
    deadline_time = BigIntegerField(null=True)
    realization_time = BigIntegerField(null=True, default=None)
    creation_time = BigIntegerField()

    comment = CharField(default='')
    period = BigIntegerField(null=True)

    # Chat will be organized later. But we are planning to create a new
    # relations table that will be holding task id, message id (not necessary),
    # message time in milliseconds, it's user id, and message itself


class UserProjectRelation(BaseModel):
    """
    This class is class for connecting projects and users, because one user can
    have more then one project, and one project can have multiple users. From it
    we can extract projects that current user have or users, that current
    project have.
    """

    user = IntegerField()
    project = ForeignKeyField(Project, related_name='project')


class _PsqlConfigChoices:
    NAME = 'NAME'
    USER = 'USER'
    HOST = 'HOST'
    PASSWORD = 'PASSWORD'
    PORT = 'PORT'


# Maybe it is wise to create another relations table with the time rules and etc
# but for not we have only deadline time. So simple.
class Adapter:

    _db_initialized = False

    def __init__(self, uid, db_name=None,
                 psql_config=None, connect_url=None):
        """
        Init for db adapter. You should select which db you will be using (from
        file sqlite or postgresql)
        :param uid: User id
        :param db_name: Name for sqlite db file, if you want to use it (if none
        of database is selected then sqlite default db in memory will be created
        )
        :param psql_config: Config dict for postgresql configuration or None.
        This is the example of this dict:
         {
            'NAME': 'mydb',
            'USER': 'shaft',
            'HOST': '/var/run/postgresql',
            'PASSWORD': '',
            'PORT': '5432'
         }
        """
        self.uid = uid

        if db_name and psql_config:
            raise db_e.DatabaseConfigureError(
                db_e.DatabaseMessages.MULTIPLE_DATABASE_SELECTION)

        elif psql_config:
            self.psql_config = psql_config

            if not Adapter._db_initialized:
                self._db_psql_initialize()
                Adapter._db_initialized = True

            self._init_psql_tables()

        elif connect_url:
            self.connect_url = connect_url

            if not Adapter._db_initialized:
                self._db_connect_initialize()
                Adapter._db_initialized = True

            self._init_psql_tables()

        else:
            if db_name is None:
                db_name = db_filename

            self.db_name = db_name
            self._db_exists = os.path.exists(self.db_name)

            if not Adapter._db_initialized:
                self._db_sqlite_initialize()
                Adapter._db_initialized = True

            if not self._db_exists:
                self._create_sqlite_database()

                # but this will never be used later
                self._db_exists = True

    # sqlite methods
    @staticmethod
    def _create_sqlite_database():
        User.create_table()
        Project.create_table()
        UserProjectRelation.create_table()
        Task.create_table()
        Message.create_table()
        logger.debug("Database created")

    def _db_sqlite_initialize(self):
        db = SqliteDatabase(self.db_name)
        _db_proxy.initialize(db)

    def _db_sqlite_exists(self):
        return os.path.exists(self.db_name)

    # postgresql methods
    @staticmethod
    def _init_psql_tables():
        if not User.table_exists():
            User.create_table()
        if not Project.table_exists():
            Project.create_table()
        if not UserProjectRelation.table_exists():
            UserProjectRelation.create_table()
        if not Task.table_exists():
            Task.create_table()
        if not Message.table_exists():
            print(123)
            Message.create_table()

        logger.debug("Database tables initialized")

    def _db_psql_initialize(self):
        try:
            db = PostgresqlDatabase(self.psql_config[_PsqlConfigChoices.NAME],
                                    user=self.psql_config[_PsqlConfigChoices.USER],
                                    password=self.psql_config[_PsqlConfigChoices.PASSWORD],
                                    host=self.psql_config[_PsqlConfigChoices.HOST],
                                    port=self.psql_config[_PsqlConfigChoices.PORT])
        except KeyError:
            raise db_e.DatabaseConfigureError(
                db_e.DatabaseMessages.INVALID_PSQL_CONFIG)

        _db_proxy.initialize(db)

    def _db_connect_initialize(self):
        db = db_url.connect(self.connect_url)
        _db_proxy.initialize(db)
