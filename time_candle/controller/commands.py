from model.model_logic.project_logic import ProjectLogic
from model.model_logic.task_logic import TaskLogic
from model.model_logic.user_logic import UserLogic
import controller.validators as v
import exceptions.validation_exceptions as v_e
from model import logger
from enums.status import key_status_dict
from enums.priority import key_priority_dict
from copy import copy
import model.time_formatter
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case and conversion to the primary entities.
Note, that we have to login anytime firstly before the actions from the user
"""


class Controller:

    def __init__(self, db_file=None):
        self.user_logic = UserLogic(db_file)
        self.task_logic = TaskLogic(db_file)
        self.project_logic = ProjectLogic(db_file)

    def log_in(self, login, password):
        """
        This function writes current user to the config.ini
        :type login: String
        :type password: String
        :return: Bool
        """
        return self.user_logic.log_in(login, password)

    def add_user(self,
                 login,
                 password,
                 mail=None,
                 nickname=None,
                 about=''):
        """
        This function adds user to the database, if there is no users with given
        login
        :type login: String
        :type password: String
        :type mail: String
        :type nickname: String
        :type about: String
        :return: None
        """
        if mail is not None:
            v.check_mail(mail)

        if nickname is None:
            nickname = login

        if not about:
            about = 'Hello, it\'s me, ' + nickname

        v.check_login(login)
        v.check_name(nickname)
        v.check_password(password)
        self.user_logic.add_user(login, password, nickname, about, mail)

    def add_user_to_project(self, login, pid):
        """
        This function adds user to the project, if our logged user is admin of the
        project
        :param login: User's login
        :param pid: Project's id
        :return: None
        """
        self.project_logic.add_user_to_project(login, pid)

    def add_project(self, title, description, members):
        """
        This function adds a new project to the database with the creator from
        logged user
        :param description: Project's description
        :param title: Project's title
        :param members: Users that will be added automatically with the creator
        :return: None
        """
        self.project_logic.add_project(title, description, members)

    def add_task(self,
                 title,
                 priority,
                 status,
                 time,
                 parent_id,
                 comment,
                 pid,
                 receiver_login,
                 period):
        """
        This function will add passed task to the database, with the creator and
        executor that named in the config.ini (i.e current logged user)
        :param pid: Project's id
        :param receiver_login: User's login
        :param comment: Task's comment for some detailed explanation
        :param parent_id: Parent's task id
        :param time: Time in following format: YYYY-MM-DD HH:MM:SS
        :param title: Task's title
        :param priority: Task's priority (enum from Priority)
        :param status: Task's status (enum from Status)
        :param period: Task's period in hours TODO:some format?
        :type pid: Int
        :type receiver_login: String
        :type comment: String
        :type parent_id: Int
        :type time: String
        :type title: String
        :type priority: Int
        :type status: Int
        :type period: String TODO: string?
        :return: None
        """
        if priority is None:
            logger.debug('Default priority has been set')
            priority = key_priority_dict['medium']
        else:
            try:
                priority = key_priority_dict[priority]
            except KeyError:
                raise v_e.InvalidPriorityError(
                    v_e.PriorityMessages.INVALID_PRIORITY)

        if status is None:
            logger.debug('Default status has been set')
            status = key_status_dict['in_progress']
        else:
            try:
                status = key_status_dict[status]
            except KeyError:
                raise v_e.InvalidStatusError(v_e.StatusMessages.INVALID_STATUS)

        if time is not None:
            time = model.time_formatter.get_milliseconds(time)

        # if period not is none we convert it to the milliseconds
        if period is not None:
            period = model.time_formatter.days_to_milliseconds(period)

        v.check_comment(comment)
        v.check_title(title)

        self.task_logic.add_task(title,
                                 priority,
                                 status,
                                 time,
                                 parent_id,
                                 comment,
                                 pid,
                                 receiver_login,
                                 period)

    def remove_task(self, tid):
        """
        This function removes selected task and it's all childs recursively or
        raises an exception if task does not exists
        :param tid: Task's id
        :return: None
        """
        self.task_logic.remove_task(tid)

    def remove_project(self, pid):
        """
        This function removes selected project or raises an exception if project
        does not exists or you simply don't have rights to do that
        :param pid: Project's id
        :return: None
        """
        self.project_logic.remove_project(pid)

    def remove_user_from_project(self, login, pid):
        """
        This function removes selected user from the project or raises an exception
        if user does not exists or you simply don't have rights to do that. Note
        that you can delete yourself from the project
        :param login: User's login
        :param pid: Project's id
        :return: None
        """
        self.project_logic.remove_user_from_project(login, pid)

    def change_task(self, tid, priority, status, time, comment, project):
        """
        This function will change task in the database, with the creator and
        executor that named in the config.ini (i.e current logged user)
        :param tid: Task's id
        :param comment: Task's comment for some detailed explanation
        :param time: Time in following format: YYYY-MM-DD HH:MM:SS
        :param priority: Tasks priority (enum from Priority)
        :param status: Tasks status (enum from Status)
        :param project: Project related to task or None
        :return: None
        """
        if priority is not None:
            try:
                priority = key_priority_dict[priority]
            except KeyError:
                raise v_e.InvalidPriorityError(
                    v_e.PriorityMessages.INVALID_PRIORITY)

        if status is not None:
            try:
                status = key_status_dict[status]
            except KeyError:
                raise v_e.InvalidStatusError(v_e.StatusMessages.INVALID_STATUS)

        if time is not None:
            time = model.time_formatter.get_milliseconds(time)

        v.check_comment(comment)

        self.task_logic.change_task(tid, priority, status, time, comment, project)

    def change_project(self, pid, title, description):
        """
        This function will change task in the database, with the creator and
        executor that named in the config.ini (i.e current logged user)
        :param pid: Project's id
        :param title: Project's title
        :param description: Project's short (or long) description
        :return: None
        """
        v.check_title(title)
        self.project_logic.change_project(pid, title, description)

    def get_tasks(self, fil):
        """
        This function returns specific tasks that was taken from the database from
        your available tasks by the filter.
        :param fil: Filter with specific syntax
        :type fil: String
        :return: list of TaskInstance
        """
        return self.task_logic.get_tasks(fil)

    def get_users(self, substr, pid=None):
        """
        This function returns found users.
        :param substr: Filter for nickname search
        :param pid: Project's id in where to search users
        :type substr: String
        :type pid: Int
        :return: list of UserInstance
        """
        return self.user_logic.get_users(substr, pid)

    def get_current_user(self):
        """
        This function returns current user.
        :return: UserInstance
        """
        user = self.user_logic.user
        return copy(user)

    def get_projects(self, substr):
        """
        This function returns found projects for your user.
        :param substr: Filter for title search
        :type substr: String
        :return: list of ProjectInstance
        """
        return self.project_logic.get_projects(substr)

    def logout(self):
        """
        This function logging out current user.
        :return: None
        """
        self.user_logic.logout()
