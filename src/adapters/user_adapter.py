from main_instances.user import User as UserModel
from adapters.task_adapter import Task
from peewee import *


class User(Model):
    # user fields
    # for UserModel's own_tasks we have a relation field in Task class from
    # adapters.task_adapter

    # TODO: Nani???
    # projects = []
    uid = IntegerField()
    login = CharField()

    # settings field
    password = CharField()
    mail = CharField()
    nickname = CharField()

    # time_zone will be saved in the form of shift in milliseconds
    time_zone = IntegerField()
    about = CharField()


class UserProjectRelation(Model):
    """
    This class is class for connecting projects and users, because one user can
    have more then one project, and one project can have multiple users
    """
    pass
