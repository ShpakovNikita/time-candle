import argparse
from collections import namedtuple
from model import commands
import app_logger

logger = app_logger.custom_logger('controller')


class _Args:
    """
    This class is used for argument parser to provide more usable form of
    parameters
    """
    Argument = namedtuple('Argument', ['long', 'short', 'docstring'])

    action = Argument(long='action', short='a', docstring=None)
    prefix_chars = Argument(long='--', short='-', docstring=None)

    # add_user tree arguments
    ADD_USER = Argument(long='adduser',
                        short='u',
                        docstring="""This argument adds a new user to the 
                        database or project, according to the given login and 
                        password, if it possible""")

    # TODO: low priority if not admin and etc.
    PROJECT = Argument(long='project',
                       short='o',
                       docstring="""This argument adds a selected user from 
                       database by login to the selected project. Specify by 
                       project's id. If used in the addtask command specify
                       two arguments, the first argument is project id, and the 
                       second one is user login. If no user specified, task will
                       be created for logged user""")

    # login tree arguments
    LOGIN = Argument(long='login',
                     short='l',
                     docstring="""This argument make next sessions from the 
                     logged users, i. e. add tasks, show their tasks etc.""")

    # add_project tree arguments
    ADD_PROJECT = Argument(long='addproject',
                           short='p',
                           docstring="""This argument adds a new project with 
                           the admin from the name of current user""")
    # TODO: maybe delete creator id to have more flexible rights (but it's hard)

    # project members
    MEMBERS = Argument(long='members',
                       short='m',
                       docstring="""This argument specify logins of the users
                       that will be added to the project""")

    # project description
    DESCRIPTION = Argument(long='description',
                           short='d',
                           docstring="""This argument allows to specify project's
                           description""")

    # add_task tree arguments
    ADD_TASK = Argument(long='addtask',
                        short='t',
                        docstring="""This argument adds a new task to the user 
                        or project""")
    # task priority
    PRIORITY = Argument(long='priority',
                        short='r',
                        docstring="""task\'s priority, that can be changed 
                        later""")

    # task time
    TIME = Argument(long='time',
                    short='t',
                    docstring="""task\'s time, can be changed later. If not 
                    passed, then time is not determent. Format is 
                    YYYY-MM-DD HH:MM:SS or simple HH:MM:SS""")

    # task status
    STATUS = Argument(long='status',
                      short='s',
                      docstring="""task\'s status, that can be changed later""")

    # task comment
    COMMENT = Argument(long='comment',
                       short='m',
                       docstring="""task\'s comment for short explanations, up 
                       to 255 symbols""")

    # task parent
    PARENT = Argument(long='parent',
                      short='p',
                      docstring="""task\'s parent. This is need for dividing
                      tasks on sub tusks. Parent's low plank of priority and
                      status marks on it's all childs. To create parent task
                      pass parent's id to this argument""")

    """
    Also project argument
    """

    # remove task
    REMOVE_TASK = Argument(long='removetask',
                           short='rm',
                           docstring="""Remove task from the database by id""")

    # change task
    CHANGE_TASK = Argument(long='changetask',
                           short='c',
                           docstring="""Changing one of the possible values to 
                           the task by it's id and optional parameters""")

    # show tasks
    # TODO: special parser syntax?
    SHOW_TASKS = Argument(long='showtasks',
                          short='s',
                          docstring="""Show all available tasks to the current 
                          person, including tasks where he is a creator. To 
                          show some type of sorted tasks, see the special 
                          parser syntax""")

    # show tasks filter
    FILTERS = Argument(long='filters',
                       short='f',
                       docstring="""Filter all available tasks by one 
                       expression with own syntax""")

    # TODO: filter will replace this argument?
    ALL_TASKS = Argument(long='all',
                         short='a',
                         docstring="""If this flag is set, we will show all 
                         tasks, with the project user's tasks""")

    PLANNER = Argument(long='planner',
                       short='l',
                       docstring="""In this argument you may pass up to 7 unique
                       numbers from 0 to 6 by the spaces. This will allow you to
                       make task planner, with the period of 7 days (weekly 
                       tasks). Also it conflicts with period argument.""")

    PERIOD = Argument(long='period',
                      short='e',
                      docstring="""This argument made for periodical tasks. You 
                      should pass one string parameter in format * * *, where 
                      first star is day, second is week, third is month. Star as
                      argument means 'every'. Example: 
                      0 * * - every first day of the every week in every month.
                      1 4 * - every second day of 5th week every month. But be 
                      sure, if there is a 28 days in the month, it can be in the
                      29 day in terms of current month. In this case task will 
                      not be shown in this month.Also it conflicts with planner 
                      argument.""")

    """
    Also project argument
    """

    # clear_log tree arguments
    CLEAR_LOG = Argument(long='clearlog',
                         short='l',
                         docstring="""This argument clears output logs""")

    # logout tree arguments
    LOGOUT = Argument(long='logout',
                      short='u',
                      docstring="""This argument logouts current user""")

    # TODO: split_task?
    # TODO: alias?
    _with_prefix = None

    @staticmethod
    def prefix():
        """
        This method generate new Args object but with prefix characters. This
        can be used in optional arguments
        :return: Args object
        """
        if _Args._with_prefix is None:
            _Args._with_prefix = _Args()
            for key in dir(_Args._with_prefix):
                # change only upper register fields
                if key.isupper():
                    value = getattr(_Args, key)
                    new_value = _Args.Argument(_Args.prefix_chars.long +
                                               value.long,
                                               _Args.prefix_chars.short +
                                               value.short,
                                               value.docstring)
                    setattr(_Args._with_prefix, key, new_value)

        return _Args._with_prefix


def run():
    """
    This function runs parser module to parse command line arguments and form
    specific requests to our main model
    :return: None
    """
    parser = argparse.ArgumentParser(prog='time_candle')

    # root_args is the main command arguments, that defines next action
    root_args = parser.add_subparsers(dest=_Args.action.long,
                                      help='sub-command help')

    # for each command initialize parser and it's specific arguments
    # TODO: check the description and help difference
    _init_add_user_parser(root_args)
    _init_add_task_parser(root_args)
    _init_login_parser(root_args)
    _init_add_project_parser(root_args)
    _init_change_task_parser(root_args)
    _init_remove_task_parser(root_args)
    _init_show_tasks_parser(root_args)

    # simple clear log arg
    root_args.add_parser(_Args.CLEAR_LOG.long,
                         help=_Args.CLEAR_LOG.docstring)

    # simple logout arg
    root_args.add_parser(_Args.LOGOUT.long,
                         help=_Args.LOGOUT.docstring)

    parsed = parser.parse_args()
    logger.debug(parsed)

    # try to process each command
    if parsed.action == _Args.ADD_USER.long:
        _process_add_user(parsed)

    elif parsed.action == _Args.LOGIN.long:
        _process_login(parsed)

    elif parsed.action == _Args.ADD_TASK.long:
        _process_add_task(parsed)

    elif parsed.action == _Args.CLEAR_LOG.long:
        open(app_logger.LOG_FILENAME, 'w').close()
        logger.info('log has been cleared')

    elif parsed.action == _Args.LOGOUT.long:
        _process_logout()

    elif parsed.action == _Args.ADD_PROJECT.long:
        _process_add_project(parsed)

    elif parsed.action == _Args.CHANGE_TASK.long:
        _process_change_task(parsed)

    elif parsed.action == _Args.REMOVE_TASK.long:
        _process_remove_task(parsed)

    elif parsed.action == _Args.SHOW_TASKS.long:
        _process_show_tasks(parsed)


"""
The functions below are private. So do not use it int any cases outside this 
commands parser module.
"""


# Initialize parsers


def _init_add_user_parser(root_args):
    # create new parser for adduser command
    user = root_args.add_parser(_Args.ADD_USER.long,
                                help=_Args.ADD_USER.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')
    user.add_argument('--password', '-p',
                      help='user password', default='')

    user.add_argument(_Args.prefix().PROJECT.long,
                      _Args.prefix().PROJECT.short,
                      help=_Args.PROJECT.docstring,
                      nargs=1)


def _init_add_task_parser(root_args):
    # create new parser for addtask command
    task = root_args.add_parser(_Args.ADD_TASK.long,
                                help=_Args.ADD_TASK.docstring)

    task.add_argument('title', help='task\'s title')
    task.add_argument(_Args.prefix().PRIORITY.long,
                      _Args.prefix().PRIORITY.short,
                      help=_Args.PRIORITY.docstring,
                      nargs=1,
                      default=[None])

    task.add_argument(_Args.prefix().STATUS.long,
                      _Args.prefix().STATUS.short,
                      help=_Args.STATUS.docstring,
                      nargs=1,
                      default=[None])

    task.add_argument(_Args.prefix().TIME.long,
                      _Args.prefix().TIME.short,
                      help=_Args.TIME.docstring,
                      nargs=1)

    task.add_argument(_Args.prefix().PARENT.long,
                      _Args.prefix().PARENT.short,
                      help=_Args.PARENT.docstring,
                      type=int,
                      nargs=1)

    # TODO: todo, you know?
    task.add_argument(_Args.prefix().PROJECT.long,
                      _Args.prefix().PROJECT.short,
                      help=_Args.PROJECT.docstring,
                      nargs='+')

    task.add_argument(_Args.prefix().COMMENT.long,
                      _Args.prefix().COMMENT.short,
                      help=_Args.COMMENT.docstring,
                      default=[''],
                      nargs=1)

    task.add_argument(_Args.prefix().PERIOD.long,
                      _Args.prefix().PERIOD.short,
                      help=_Args.PERIOD.docstring,
                      default=[None],
                      nargs='+')

    task.add_argument(_Args.prefix().PLANNER.long,
                      _Args.prefix().PLANNER.short,
                      help=_Args.PLANNER.docstring,
                      default=[None],
                      nargs=1)


def _init_remove_task_parser(root_args):
    # create new parser for removetask command
    task = root_args.add_parser(_Args.REMOVE_TASK.long,
                                help=_Args.REMOVE_TASK.docstring)

    task.add_argument('id', help='task\'s id to delete from database')


def _init_change_task_parser(root_args):
    # create new parser for changetask command
    task = root_args.add_parser(_Args.CHANGE_TASK.long,
                                help=_Args.CHANGE_TASK.docstring)

    task.add_argument('id', help='task\'s id to change from database')
    task.add_argument(_Args.prefix().PRIORITY.long,
                      _Args.prefix().PRIORITY.short,
                      help=_Args.PRIORITY.docstring,
                      nargs=1)

    task.add_argument(_Args.prefix().STATUS.long,
                      _Args.prefix().STATUS.short,
                      help=_Args.STATUS.docstring,
                      nargs=1)

    task.add_argument(_Args.prefix().TIME.long,
                      _Args.prefix().TIME.short,
                      help=_Args.TIME.docstring,
                      nargs=1)

    task.add_argument(_Args.prefix().COMMENT.long,
                      _Args.prefix().COMMENT.short,
                      help=_Args.COMMENT.docstring,
                      default=[None],
                      nargs=1)


def _init_add_project_parser(root_args):
    # create new parser for addproject command
    project = root_args.add_parser(_Args.ADD_PROJECT.long,
                                   help=_Args.ADD_PROJECT.docstring)

    project.add_argument('title', help='project\'s title')
    project.add_argument(_Args.prefix().MEMBERS.long,
                         _Args.prefix().MEMBERS.short,
                         help=_Args.MEMBERS.docstring,
                         nargs='+',
                         default=[])

    project.add_argument(_Args.prefix().DESCRIPTION.long,
                         _Args.prefix().DESCRIPTION.short,
                         help=_Args.DESCRIPTION.docstring,
                         nargs=1,
                         default=[''])


def _init_login_parser(root_args):
    # create new parser for login command
    user = root_args.add_parser(_Args.LOGIN.long,
                                help=_Args.LOGIN.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')
    user.add_argument('password', help='user password')


def _init_show_tasks_parser(root_args):
    # create new parser for login command
    show = root_args.add_parser(_Args.SHOW_TASKS.long,
                                help=_Args.SHOW_TASKS.docstring)

    # TODO: now we count nargs + as 1
    show.add_argument(_Args.prefix().PROJECT.long,
                      _Args.prefix().PROJECT.short,
                      help=_Args.PROJECT.docstring,
                      nargs='+',
                      default=[])

    show.add_argument(_Args.prefix().FILTERS.long,
                      _Args.prefix().FILTERS.short,
                      help=_Args.FILTERS.docstring,
                      nargs=1)

    show.add_argument(_Args.prefix().ALL_TASKS.long,
                      _Args.prefix().ALL_TASKS.short,
                      help=_Args.ALL_TASKS.docstring,
                      action='store_true')


# Process parsed arguments
# TODO: Change everything on getattr


def _process_login(parsed_args):
    logger.debug('login')
    commands.log_in(parsed_args.login, parsed_args.password)


def _process_add_task(parsed_args):
    logger.debug('add_task')

    # time, parent and comment is list value, so we have to extract data from it
    time = None
    if parsed_args.time is not None:
        time = parsed_args.time[0]

    parent = None
    if parsed_args.parent is not None:
        parent = parsed_args.parent[0]

    # TODO: multiple times
    if parsed_args.project is None:
        commands.add_task(parsed_args.title,
                          parsed_args.priority[0],
                          parsed_args.status[0],
                          time,
                          parent,
                          parsed_args.comment[0],
                          None,
                          None)

    else:
        # set the uid None if it is not in the list
        if len(parsed_args.project) == 1:
            uid = None

        else:
            uid = parsed_args.project[1]

        commands.add_task(parsed_args.title,
                          parsed_args.priority[0],
                          parsed_args.status[0],
                          time,
                          parent,
                          parsed_args.comment[0],
                          parsed_args.project[0],
                          uid)


def _process_change_task(parsed_args):
    logger.debug('change_task')

    # time and comment is list value, so we have to extract data from it
    time = None
    if parsed_args.time is not None:
        time = parsed_args.time[0]

    commands.change_task(parsed_args.id,
                         parsed_args.priority,
                         parsed_args.status,
                         time,
                         parsed_args.comment[0])


def _process_remove_task(parsed_args):
    logger.debug('remove_task')
    commands.remove_task(parsed_args.id)


def _process_logout():
    commands.logout()
    

def _process_add_user(parsed_args):
    logger.debug('add_user')
    if parsed_args.project is None:
        if parsed_args.password == '':
            raise ValueError('You must specify the password!')

        commands.add_user(parsed_args.login, parsed_args.password)

    else:
        commands.add_user_to_project(parsed_args.login, parsed_args.project)


def _process_add_project(parsed_args):
    logger.debug('add_project')
    commands.add_project(parsed_args.title,
                         parsed_args.description[0],
                         parsed_args.members)


def _process_show_tasks(parsed_args):
    commands.show_tasks(parsed_args.project, parsed_args.all)
