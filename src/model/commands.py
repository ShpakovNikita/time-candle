import model.model_logic.project_logic as project
import model.model_logic.task_logic as task
import model.model_logic.user_logic as user
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case and conversion to the primary entities.
Note, that we have to login anytime firstly before the actions from the user
"""


def log_in(login, password):
    """
    This function writes current user to the config.ini
    :type login: String
    :type password: String
    :return: None
    """
    user.log_in(login, password)


def add_user(login, password):
    """
    This function adds user to the database, if there is no users with given
    login
    :type login: String
    :type password: String
    :return: None
    """
    user.add_user(login, password)


def add_user_to_project(login, pid):
    """
    This function adds user to the project, if our logged user is admin of the
    project
    :param login: User's login
    :param pid: Project's id
    :return: None
    """
    project.add_user_to_project(login, pid)


def add_project(title, description, members):
    """
    This function adds a new project to the database with the creator from
    logged user
    :param description: Project's description
    :param title: Project's title
    :param members: Users that will be added automatically with the creator
    :return: None
    """
    project.add_project(title, description, members)


def add_task(title,
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
    task.add_task(title, priority, status, time, parent_id, comment, pid, login)


def remove_task(tid):
    """
    This function removes selected task and it's all childs recursively or
    raises an exception if task does not exists
    :param tid: Tasks id
    :return: None
    """
    task.remove_task(tid)


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
    task.change_task(tid, priority, status, time, comment)


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
    # TODO: Change on get tasks, FULLY UNWORKABLE NOW

    if len(projects) == 0:
        # print user's personal task's
        tids = Adapters.USER_ADAPTER.get_tasks_id_by_uid(
            Singleton.GLOBAL_USER.uid)
        for tid in tids:
            _print_task(tid)

    else:
        if all_flag:
            # print all tasks
            pass

        for project in projects:
            _print_project_tasks(project)


def logout():
    user.logout()


def _print_project_tasks(pid):
    pass


# TODO: remove
def _print_task(tid, is_project=False):
    """
    This function print's task info
    :param tid: Task's id to print
    :param is_project: If flag specified then we will be printing users too
    :return: None
    """
    task = TaskInstance.make_task(Adapters.TASK_ADAPTER.get_task_by_id(tid))
    print()
    print('Task ' + task.title)
    print('Task\'s id is ' + str(task.tid))
    if is_project:
        print('The task creator: ' +
              UserInstance.make_user(
                  Adapters.USER_ADAPTER.get_user_by_id(task.creator_uid).
                      nickname))
        print('The task receiver: ' +
              UserInstance.make_user(
                  Adapters.USER_ADAPTER.get_user_by_id(task.uid).nickname))

    if task.deadline is None:
        task_time = 'unlimited'
    else:
        task_time = validators.get_datetime(task.deadline). \
            strftime('%Y-%m-%d %H:%M:%S')

    print('Task\'s deadline time is ' + task_time)
    # print priority etc
