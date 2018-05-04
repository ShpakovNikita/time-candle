from storage.adapter_classes import Task, User
import storage
from main_instances.task import Task as TaskInstance
import app_logger
import exceptions.db_exceptions
from singleton import Singleton
from peewee import *


def save(task):
    """
    This function is used to store given task to the database. Note, that tasks
    can be with similar names and dates (but on that case I have a task below)
    TODO: warning if the task's title and time are matching with some precision
    :param task: This is our task to save
    :type task: TaskInstance
    :return: None
    """

    # This code is checking is our parent tid exists in the database for logged
    # user
    if task.parent is not None:
        _get_task_by_id(task.parent)

    table_task = Task.create(creator=task.creator_uid,
                             receiver=task.uid,
                             project=None,
                             status=task.status,
                             # task.parent looks more beautiful then tid
                             parent=task.parent,
                             title=task.title,
                             priority=task.priority,
                             deadline_time=task.deadline,
                             comment=task.comment)

    app_logger.custom_logger('storage').debug('taks\'s parent %s' %
                                              table_task.parent)

    app_logger.custom_logger('storage').debug('task saved to database')


def last_id():
    """
    This function gets last id to add task on it's place
    TODO:
    This function finds the first unused id in the table to add new task row on
    that place
    :return: Int
    """

    query = Task.select().order_by(Task.id.desc())
    app_logger.custom_logger('storage').debug('getting last id from query...{}'
                                              .format(query))

    try:
        return query.get().id

    except DoesNotExist:
        return 1


def _get_task_by_id(tid):
    """
    This function finds task by id and current user in database and returns it,
    or raise error due to incorrect request
    :param tid: Task id to find
    :type tid: Int
    :return: Task (storage class)
    """
    # TODO: more flexible user dependency find for projects
    task = Task.select().where((Task.id == tid) &
                               ((Task.creator == Singleton.GLOBAL_USER.uid) |
                                (Task.receiver == Singleton.GLOBAL_USER.uid)))
    try:
        return task.get()

    except DoesNotExist:
        msg = 'There is no such tid %s in the database for your user' % tid
        raise exceptions.db_exceptions.InvalidTidError(msg)
