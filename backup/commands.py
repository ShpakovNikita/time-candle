from enums.status import Status
from enums.priority import Priority
from model.main_instances.task import Task as TaskInstance
from model.main_instances import Project as ProjectInstance
from storage import *
import storage.adapter_classes
import storage.task_adapter
import storage.user_adapter
import storage.project_adapter
import exceptions.db_exceptions as db_e
from model import validators, config_parser
from model.session_control import Singleton
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case and conversion to the primary entities.
Note, that we have to login anytime firstly before the actions from the user
"""


logger = app_logger.custom_logger('model')


def log_in(login, password):
    """
    This function writes current user to the config.ini
    :type login: String
    :type password: String
    :return: None
    """
    storage.user_adapter.login_user(login, password)
    # if everything is ok, we will write our login and password to the
    # config.ini
    config_parser.write_user(login, password)


def add_user(login, password):
    """
    This function adds user to the database, if there is no users with given
    login
    :type login: String
    :type password: String
    :return: None
    """
    storage.user_adapter.add_user(login, password)


def add_user_to_project(login, pid):
    """
    This function adds user to the project, if our logged user is admin of the
    project
    :param login: User's login
    :param pid: Project's id
    :return: None
    """
    # get user from config.ini to make our project from it's name
    Singleton.GLOBAL_USER = _login()

    storage.user_adapter.add_user_to_project_by_id(login, pid)


def add_project(title, description, members):
    """
    This function adds a new project to the database with the creator from
    logged user
    :param description: Project's description
    :param title: Project's title
    :param members: Users that will be added automatically with the creator
    :return: None
    """

    # TODO: make it to the final!
    # get user from config.ini to make our project from it's name
    user = _login()
    Singleton.GLOBAL_USER = user

    project = ProjectInstance(storage.project_adapter.last_id() + 1,
                              user.uid,
                              title,
                              description)

    storage.project_adapter.save(project)

    try:
        for login in members:
            add_user_to_project(login, project.pid)

    except db_e.InvalidLoginError:
        storage.project_adapter.remove_project_by_id(project.pid)
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)


# TODO: THERE IS REALLY BIG DUPLICATED CODE. ASK ANDY WHAT IS OK
def add_task(title, priority, status, time, parent_id, comment):
    """
    This function will add passed task to the database, with the creator and
    executor that named in the config.ini (i.e current logged user)
    :param comment: Task's comment for some detailed explanation
    :param parent_id: Parent's task id
    :param time: Time in following format: YYYY-MM-DD HH:MM:SS
    :param title: Tasks title
    :param priority: Tasks priority (enum from Priority)
    :param status: Tasks status (enum from Status)
    :type comment: String
    :type parent_id: Int
    :type time: String
    :type title: String
    :type priority: Int
    :type status: Int
    :return: None
    """
    # get user from config.ini to make our task from it's name
    user = _login()
    Singleton.GLOBAL_USER = user

    # This max func needed to set tasks status and priority not lower then
    # parent's
    if priority is None:
        logger.debug('Default priority has been set')
        priority = Priority.MEDIUM

    if status is None:
        logger.debug('Default status has been set')
        status = Status.IN_PROGRESS

    # This code is also checking is our parent tid exists in the database for
    # logged user. The max func needed to set tasks status and priority not
    # lower then parent's

    if parent_id is not None:
        parent_task = storage.task_adapter.get_task_by_id(parent_id)
        status = max(status, parent_task.status)
        priority = max(priority, parent_task.priority)

    deadline_time = None

    if time is not None:
        deadline_time = validators.get_milliseconds(time)

    logger.debug('time in milliseconds %s' % deadline_time)

    task = TaskInstance(user.uid,
                        user.uid,
                        storage.task_adapter.last_id() + 1,
                        deadline_time,
                        title,
                        None,
                        status,
                        priority,
                        parent_id,
                        comment)

    logger.debug('task configured and ready to save , the task id is %s'
                 % task.tid)

    storage.task_adapter.save(task)


def add_task_to_project(title,
                        priority,
                        status,
                        time,
                        parent_id,
                        comment,
                        pid,
                        login):
    """
    This function will add passed task to the database, with the creator and
    executor that named in the config.ini (i.e current logged user)
    :param pid: Project's id
    :param login: User's login
    :param comment: Task's comment for some detailed explanation
    :param parent_id: Parent's task id
    :param time: Time in following format: YYYY-MM-DD HH:MM:SS
    :param title: Tasks title
    :param priority: Tasks priority (enum from Priority)
    :param status: Tasks status (enum from Status)
    :type pid: Int
    :type login: String
    :type comment: String
    :type parent_id: Int
    :type time: String
    :type title: String
    :type priority: Int
    :type status: Int
    :return: None
    """
    # get user from config.ini to make our task from it's name
    user = _login()
    Singleton.GLOBAL_USER = user

    # This max func needed to set tasks status and priority not lower then
    # parent's
    if priority is None:
        logger.debug('Default priority has been set')
        priority = Priority.MEDIUM

    if status is None:
        logger.debug('Default status has been set')
        status = Status.IN_PROGRESS

    # This code is also checking is our parent tid exists in the database for
    # logged user. The max func needed to set tasks status and priority not
    # lower then parent's

    # TODO: parent pid match pid
    if parent_id is not None:
        parent_task = storage.task_adapter.get_task_by_id(parent_id, pid)
        status = max(status, parent_task.status)
        priority = max(priority, parent_task.priority)

    deadline_time = None

    if time is not None:
        deadline_time = validators.get_milliseconds(time)

    logger.debug('time in milliseconds %s' % deadline_time)

    # TODO: MADE NOT ONLY ADMIN ADD, BUT USERS WITH LOW PRIORITY!!! Just change
    # TODO: on is_admin(pid) maybe

    # Check for rights and id's
    if login is None:
        task_uid = user.uid
    else:
        storage.user_adapter.is_user_in_project(login, pid)
        task_uid = storage.user_adapter.get_id_by_login(login)

    storage.project_adapter.has_rights(pid)

    task = TaskInstance(task_uid,
                        user.uid,
                        storage.task_adapter.last_id() + 1,
                        deadline_time,
                        title,
                        pid,
                        status,
                        priority,
                        parent_id,
                        comment)

    logger.debug('task configured and ready to save , the task id is %s'
                 % task.tid)

    storage.task_adapter.save(task)

    logger.debug('task to project added')


def remove_task(tid):
    """
    This function removes selected task and it's all childs recursively or
    raises an exception if task does not exists
    :param tid: Tasks id
    :return: None
    """
    storage.task_adapter.remove_task_by_id(tid)


def change_task(tid, priority, status, time, comment):
    """
    This function will change task in the database, with the creator and
    executor that named in the config.ini (i.e current logged user)
    :param tid: Task's id
    :param comment: Task's comment for some detailed explanation
    :param time: Time in following format: YYYY-MM-DD HH:MM:SS
    :param priority: Tasks priority (enum from Priority)
    :param status: Tasks status (enum from Status)
    :type tid: Int
    :type comment: String
    :type time: String
    :type priority: Int
    :type status: Int
    :return: None
    """
    # TODO: This function
    # get user from config.ini to make our task from it's name
    user = _login()
    Singleton.GLOBAL_USER = user
    pass


def show_tasks(projects, all_flag):
    """
    This function prints the tasks for current user. It will print all tasks for
    each project if he admin in it or just his tasks, and not his personal
    tasks. But if there is no projects we will print only personal tasks.
    And if all flag specified we will print all tasks that you have relation
    with.
    :param projects: all projects that will be visited to print the task
    :param all_flag: this flag shows, is we are going to show all related to you
    tasks
    :return: None
    """
    # TODO: This function
    # get user from config.ini to make our task from it's name
    user = _login()
    Singleton.GLOBAL_USER = user

    if len(projects) == 0:
        # print user's personal task's
        tids = storage.user_adapter.get_tasks_id_by_uid(user.uid)
        for tid in tids:
            _print_task(tid)

    else:
        if all_flag:
            # print all tasks
            pass

        for project in projects:

            _print_project_tasks(project)


def _print_project_tasks(pid):
    pass


def _print_task(tid, is_project=False):
    """
    This function print's task info
    :param tid: Task's id to print
    :param is_project: If flag specified then we will be printing users too
    :return: None
    """
    task = storage.task_adapter.get_task_by_id(tid)
    print()
    print('Task ' + task.title)
    print('Task\'s id is ' + str(task.tid))
    if is_project:
        print('The task creator: ' +
              storage.user_adapter.get_user_by_id(task.creator_uid).nickname)
        print('The task receiver: ' +
              storage.user_adapter.get_user_by_id(task.uid).nickname)

    if task.deadline is None:
        task_time = 'unlimited'
    else:
        task_time = validators.get_datetime(task.deadline).\
            strftime('%Y-%m-%d %H:%M:%S')

    print('Task\'s deadline time is ' + task_time)
    # print priority etc


def _login():
    """
    Returns loaded user to make some actions from it's name. User will be
    initialized from config file.
    :return: User
    """

    return config_parser.run_config()['user']
