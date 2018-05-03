from storage.adapter_classes import Task, User
import storage
from main_instances.task import Task as TaskInstance
import app_logger
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
    Task.create(creator=task.creator_uid,
                receiver=task.uid,
                project=None,
                status=task.status,
                # TODO change on id or normal task_adapter
                parent=task.parent,
                title=task.title,
                priority=task.priority,
                deadline_time=task.deadline)

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

    # Yes, it is bad to make exceptions like this
    except:
        return 1

