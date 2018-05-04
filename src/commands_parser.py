import argparse
from collections import namedtuple
import commands
import app_logger


MODULE_LOGGER_NAME = 'controller'


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

    PROJECT = Argument(long='project',
                       short='p',
                       docstring="""This argument adds a selected user from 
                       database by login to the selected project. Specify by 
                       project's id""")

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
                    docstring="""task\'s time, cannot be changed later. If
                    not passed, then time is not determent""")

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
    # TODO: low planks of priority and status
    PARENT = Argument(long='parent',
                      short='p',
                      docstring="""task\'s parent. This is need for dividing
                      tasks on sub tusks. Parent's low plank of priority and
                      status marks on it's all childs. To create parent task
                      pass parent's id to this argument""")

    # clear_log tree arguments
    CLEAR_LOG = Argument(long='clearlog',
                         short='l',
                         docstring="""This argument clears output logs""")

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

    # simple clear log arg
    root_args.add_parser(_Args.CLEAR_LOG.long,
                         help=_Args.CLEAR_LOG.docstring)

    parsed = parser.parse_args()
    app_logger.custom_logger(MODULE_LOGGER_NAME).debug(parsed)

    # try to process each command
    if parsed.action == _Args.ADD_USER.long:
        _process_add_user(parsed)

    if parsed.action == _Args.LOGIN.long:
        _process_login(parsed)

    if parsed.action == _Args.ADD_TASK.long:
        _process_add_task(parsed)

    if parsed.action == _Args.CLEAR_LOG.long:
        open(app_logger.LOG_FILENAME, 'w').close()
        app_logger.custom_logger('controller').info('log has been cleared')

    if parsed.action == _Args.ADD_PROJECT.long:
        _process_add_project(parsed)


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
    user.add_argument('password', help='user password')


def _init_add_task_parser(root_args):
    # create new parser for addtask command
    task = root_args.add_parser(_Args.ADD_TASK.long,
                                help=_Args.ADD_TASK.docstring)

    task.add_argument('title', help='task\'s title')
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

    task.add_argument(_Args.prefix().PARENT.long,
                      _Args.prefix().PARENT.short,
                      help=_Args.PARENT.docstring,
                      type=int,
                      nargs=1)

    task.add_argument(_Args.prefix().COMMENT.long,
                      _Args.prefix().COMMENT.short,
                      help=_Args.COMMENT.docstring,
                      default=[''],
                      nargs=1)


def _init_add_project_parser(root_args):
    # create new parser for addproject command
    project = root_args.add_parser(_Args.ADD_PROJECT.long,
                                   help=_Args.ADD_PROJECT.docstring)

    project.add_argument('title', help='project\'s title')
    project.add_argument(_Args.prefix().MEMBERS.long,
                         _Args.prefix().MEMBERS.short,
                         help=_Args.MEMBERS.docstring,
                         nargs='+')


def _init_login_parser(root_args):
    # create new parser for login command
    user = root_args.add_parser(_Args.LOGIN.long,
                                help=_Args.LOGIN.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')
    user.add_argument('password', help='user password')


# Process parsed arguments
# TODO: Change everything on getattr


def _process_login(parsed_args):
    app_logger.custom_logger(MODULE_LOGGER_NAME).debug('login')
    commands.log_in(parsed_args.login, parsed_args.password)


def _process_add_task(parsed_args):
    app_logger.custom_logger(MODULE_LOGGER_NAME).debug('add_task')

    # time, parent and comment is list value, so we have to extract data from it
    time = None
    if parsed_args.time is not None:
        time = parsed_args.time[0]

    parent = None
    if parsed_args.parent is not None:
        parent = parsed_args.parent[0]

    commands.add_task(parsed_args.title,
                      parsed_args.priority,
                      parsed_args.status,
                      time,
                      parent,
                      parsed_args.comment[0])


def _process_add_user(parsed_args):
    app_logger.custom_logger(MODULE_LOGGER_NAME).debug('add_user')
    commands.add_user(parsed_args.login, parsed_args.password)


def _process_add_project(parsed_args):
    app_logger.custom_logger(MODULE_LOGGER_NAME).debug('add_project')
    commands.add_project(parsed_args.title,
                         parsed_args.members)
