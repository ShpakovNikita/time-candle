from storage.adapter_classes import Task, User
import storage
from main_instances.task import Task as TaskInstance
import app_logger
import exceptions.db_exceptions as db_e
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
    try:
        Task.select().where(Task.id == task.tid).get()
        update()
        app_logger.custom_logger('storage').debug('task updated')

    except DoesNotExist:
        app_logger.custom_logger('storage').debug('adding task...')

    table_task = Task.create(creator=task.creator_uid,
                             receiver=task.uid,
                             project=task.pid,
                             status=task.status,
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


def remove_task_by_id(tid):
    """
    This function removes selected task and it's all childs recursively or
    raises an exception if task does not exists
    :param tid: Tasks id
    :return: None
    """
    # TODO: Is that good to have a recursive try except?
    try:
        query = Task.select().where(Task.parent == tid)
        for task in query:
            remove_task_by_id(task.id)

        app_logger.custom_logger('storage').info('removing task by tid %s' %
                                                 tid)
        Task.delete().where(Task.id == tid).execute()
    except DoesNotExist:
        app_logger.custom_logger('storage').info('There is no such tid %s in '
                                                 'the database for your user' %
                                                 tid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def get_task_by_id(tid):
    """
    This function finds task by id and current user in database and returns it,
    or raise error due to incorrect request
    :param tid: Task id to find
    :type tid: Int
    :return: Task
    """
    # TODO: more flexible user dependency find for projects
    task = Task.select().where((Task.id == tid) &
                               ((Task.creator == Singleton.GLOBAL_USER.uid) |
                                (Task.receiver == Singleton.GLOBAL_USER.uid)))
    try:
        return _storage_to_model(task.get())

    except DoesNotExist:
        app_logger.custom_logger('storage').info('There is no such tid %s in '
                                                 'the database for your user' %
                                                 tid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def update():
    pass


def _storage_to_model(storage_task):
    """
    This function converts storage task to model task
    :type storage_task: Task
    :return: TaskInstance
    """
    app_logger.custom_logger('storage').debug('convert storage to model task')
    # we can have a None parent, so we have to determine this to take it's id or
    # not
    if storage_task.parent is None:
        parent_id = None
    else:
        parent_id = storage_task.parent.id

    model_task = TaskInstance(storage_task.receiver.id,
                              storage_task.creator.id,
                              storage_task.id,
                              storage_task.deadline_time,
                              storage_task.title,
                              None,
                              storage_task.status,
                              storage_task.priority,
                              parent_id,
                              storage_task.comment)

    return model_task
