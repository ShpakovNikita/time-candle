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


class User(Model):
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

    class Meta:
        database = db


class Project(Model):
    title = CharField()
    admin = ForeignKeyField(User, related_name='admin')
    description = TextField()

    class Meta:
        database = db


class Task(Model):
    creator = ForeignKeyField(User, related_name='creator')

    # if the task is not project task this field equals to the creator field
    receiver = ForeignKeyField(User, related_name='receiver')

    # if the task is not project task this field equals null
    project = ForeignKeyField(User, related_name='project', null=True)
    status = SmallIntegerField()
    # TODO: Nani???
    parent = ForeignKeyField('self', null=True)

    title = CharField()
    priority = SmallIntegerField()

    # Time in milliseconds. Nullable for further functionality TODO:
    deadline_time = BigIntegerField(null=True)
    comment = CharField(default='')
    period = IntegerField(null=True)

    # Chat will be organized later. But we are planning to create a new
    # relations table that will be holding task id, message id (not necessary),
    # message time in milliseconds, it's user id, and message itself

    class Meta:
        database = db


class UserProjectRelation(Model):
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

    class Meta:
        database = db


class TagTaskRelation(Model):
    """
    This class is class for connecting search tag and tasks, because one tag can
    have more then one task, and one task can have multiple tags. From it we can
    extract tasks that current tag have or tags, that current task have. Also we
    should keep project id, because tags works only inside projects.
    """

    tag = ForeignKeyField(User, related_name='tag')
    task = ForeignKeyField(Task, related_name='tasks')
    project = ForeignKeyField(Project, related_name='project')

    class Meta:
        database = db

# Maybe it is wise to create another relations table with the time rules and etc
# but for not we have only deadline time. So simple.

# TODO: chat task relations table witch maybe messages
# TODO: role tags relations?


def _test_login(login, password):
    """
    This function checking if selected login and password matches to the
    database and if so, we make next session from the logged user's name (user
    data is written to the config file). Or we are raising an exception.
    :param login: String
    :param password: String
    :return: None
    """
    query = User.select().where(User.login == login)
    if not query.exists():
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_NOT_EXISTS)

    elif query.get().password != password:
        raise db_e.InvalidPasswordError(db_e.PasswordMessages.
                                        PASSWORD_IS_NOT_MATCH)

    # Due to this function is just for checking, it is wise to relocate lower
    # code to the inner function
    else:
        config_parser.write_user(login, password)


def _run():
    User.create_table()
    Project.create_table()
    UserProjectRelation.create_table()
    TagTaskRelation.create_table()
    Task.create_table()
    app_logger.custom_logger('storage').debug("Database created")


if new_db_flag:
    _run()
