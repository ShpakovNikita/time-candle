from peewee import *
import exceptions.db_exceptions as db_e
import os
import config_parser
import app_logger

db_filename = 'data.db'
new_db_flag = not os.path.exists(db_filename)
db = SqliteDatabase(db_filename)


class Filter:
    # Constants that show our operators
    OP_AND = 0
    OP_OR = 1

    def __init__(self):
        self.result = []
        self.ops = []

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


class Adapter:
    def __init__(self, uid):
        self._uid = uid


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    uid = PrimaryKeyField()

    # user fields
    # for UserModel's own_tasks we have a relation field in Task class from
    # storage.task_adapter

    # TODO: Nani???
    # projects [] -> see the UserProjectRelation table
    login = CharField(unique=True)

    # settings field
    password = CharField()
    mail = CharField(null=True)
    nickname = CharField(default='')

    # time_zone will be saved in the form of shift in milliseconds
    time_zone = IntegerField(default=0)
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
    project = ForeignKeyField(User, related_name='project', null=True)
    status = SmallIntegerField()
    parent = ForeignKeyField('self', null=True)

    title = CharField()
    priority = SmallIntegerField()

    # Time in milliseconds. Nullable for further functionality TODO:
    deadline_time = BigIntegerField(null=True)
    comment = CharField(default='')
    period = BigIntegerField(null=True)

    # crontab style planner?
    planner = CharField(null=True)

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

    # TODO: rights as class with the relations
    rights = CharField(default='')


class TagTaskRelation(BaseModel):
    """
    This class is class for connecting search tag and tasks, because one tag can
    have more then one task, and one task can have multiple tags. From it we can
    extract tasks that current tag have or tags, that current task have. Also we
    should keep project id, because tags works only inside projects.
    """

    tag = ForeignKeyField(User, related_name='tag')
    task = ForeignKeyField(Task, related_name='tasks')
    project = ForeignKeyField(Project, related_name='project')


# Maybe it is wise to create another relations table with the time rules and etc
# but for not we have only deadline time. So simple.

# TODO: chat task relations table witch maybe messages
# TODO: role tags relations?


def _run():
    User.create_table()
    Project.create_table()
    UserProjectRelation.create_table()
    TagTaskRelation.create_table()
    Task.create_table()
    app_logger.custom_logger('storage').debug("Database created")


if new_db_flag:
    _run()
