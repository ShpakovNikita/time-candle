import config_parser
import app_logger
from enums.status import Status
from enums.priority import Priority
from main_instances.user import User
from main_instances.task import Task as TaskInstance
import os
from storage import *
import storage.adapter_classes
import storage.task_adapter
import storage.user_adapter
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case and conversion to the primary entities.
"""


def log_in(login, password):
    """
    Writes current user to the config.ini
    :param login: string
    :param password: string
    :return: Nothing
    """
    # TODO: Yes, it is protected member and it is bad to use it
    storage.adapter_classes._test_login(login, password)


def add_user(login, password):
    # TODO: Yes, it is protected member and it is bad to use it
    storage.adapter_classes._test_add_user(login, password)
    pass


def add_task(title, priority, status, time):
    """
    This function will add passed task to the database, with the creator and
    executor that named in the config.ini (i.e current logged user)
    :param time: Time in following format: YYYY-MM-DD HH:MM:SS
    :param title: Tasks title
    :param priority: Tasks priority (enum from Priority)
    :param status: Tasks status (enum from Status)
    :type time: String
    :type title: String
    :type priority: Int
    :type status: Int
    :return: None
    """
    if priority is None:
        app_logger.custom_logger('model').debug('Default priority has been set')
        priority = Priority.MEDIUM

    if status is None:
        app_logger.custom_logger('model').debug('Default status has been set')
        status = Status.IN_PROGRESS

    # get user from config.ini to make our task from it's name
    user = _login()

    task = TaskInstance(user.uid,
                        user.uid,
                        storage.task_adapter.last_id(),
                        # TODO: real time
                        0,
                        title,
                        None,
                        status,
                        priority)

    print(task.uid)
    app_logger.custom_logger('model').debug('task configured and ready to save')

    storage.task_adapter.save(task)


def _login():
    """
    Returns loaded user to make some actions from it's name. User will be
    initialized from config file.
    :return: User
    """

    return config_parser.run_config()['user']
