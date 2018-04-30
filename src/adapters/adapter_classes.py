from peewee import *
import os
# from adapters.project_adapter import Project

db_filename = 'data.db'
new_db_flag = not os.path.exists(db_filename)
db = SqliteDatabase(db_filename)


class User(Model):
    # user fields
    # for UserModel's own_tasks we have a relation field in Task class from
    # adapters.task_adapter

    # TODO: Nani???
    # projects [] -> see the UserProjectRelation table
    login = CharField(unique=True)

    # settings field
    password = CharField()
    mail = CharField(unique=True)
    nickname = CharField()

    # time_zone will be saved in the form of shift in milliseconds
    time_zone = IntegerField()
    about = CharField()

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
    # parent = ForeignKeyField(Task, related_name='parent')

    parent = BigIntegerField()
    priority = SmallIntegerField()
    # Time in milliseconds
    deadline_time = BigIntegerField()
    comment = CharField()

    # Chat will be organized later. But we are planning to create a new
    # relations table that will be holding task id, message id (not necessary),
    # message time in milliseconds, it's user id, and message itself

    class Meta:
        database = db


class Project(Model):
    admin = ForeignKeyField(User, related_name='admin')

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
    project = ForeignKeyField(Project, related_name='projects')
    rights = SmallIntegerField()

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
    project = ForeignKeyField(Project, related_name='project', primary_key=True)

    class Meta:
        database = db

# Maybe it is wise to create another relations table with the time rules and etc
# but for not we have only deadline time. So simple.


# only test functions
def _test():
    user1 = User.create()


def _run():
    User.create_table()
    Project.create_table()
    UserProjectRelation.create_table()
    TagTaskRelation.create_table()
    Task.create_table()
    print("Database created!")

    _test()


if new_db_flag:
    _run()
