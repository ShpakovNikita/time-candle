from peewee import *
import exceptions.db_exceptions as db_e
import os
from storage import logger


db_filename = 'data.db'
new_db_flag = not os.path.exists(db_filename)
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


class Project(BaseModel):
    pid = PrimaryKeyField()

    title = CharField()
    admin = ForeignKeyField(User, related_name='admin')
    description = TextField()


class Task(BaseModel):
    tid = PrimaryKeyField()

    creator = ForeignKeyField(User, related_name='creator')

    # if the task is not project task this field equals to the creator field
    receiver = ForeignKeyField(User, related_name='receiver')

    # if the task is not project task this field equals null
    project = ForeignKeyField(Project, related_name='project', null=True)
    status = SmallIntegerField()
    parent = ForeignKeyField('self', null=True)

    title = CharField()
    priority = SmallIntegerField()

    # Time in milliseconds. Nullable for further functionality TODO:
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

    user = ForeignKeyField(User, related_name='user')
    project = ForeignKeyField(Project, related_name='project')


# Maybe it is wise to create another relations table with the time rules and etc
# but for not we have only deadline time. So simple.

# TODO: chat task relations table witch maybe messages
# TODO: role tags relations?


class Adapter:

    _db_initialized = False

    def __init__(self, uid, db_name=db_filename):
        self.uid = uid

        if db_name is None:
            db_name = db_filename

        self.db_name = db_name
        self._db_exists = os.path.exists(self.db_name)

        if not Adapter._db_initialized:
            self._db_initialize()
            Adapter._db_initialized = True

        if not self._db_exists:
            self._create_database()

            # but this will never be used later
            self._db_exists = True

    @staticmethod
    def _create_database():
        User.create_table()
        Project.create_table()
        UserProjectRelation.create_table()
        Task.create_table()
        logger.debug("Database created")

    def _db_initialize(self):
        db = SqliteDatabase(self.db_name)
        _db_proxy.initialize(db)

    def _db_exists(self):
        return os.path.exists(self.db_name)
