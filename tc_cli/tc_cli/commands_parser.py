import argparse
from collections import namedtuple
from time_candle.controller.commands import Controller as AppController
from time_candle.exceptions import AppException
from tc_cli.exceptions import AuthenticationError
import time_candle.app_logger
from tc_cli import print_functions
from tc_cli.user_controller import UserAuthenticationController as \
    UserController
from tc_cli import settings as config
import traceback


logger = time_candle.app_logger.custom_logger('console')
app_controller = None
user_controller = None


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

    # mail
    MAIL = Argument(long='mail',
                    short='m',
                    docstring="""This argument adds user email""")

    # about
    ABOUT = Argument(long='about',
                     short='f',
                     docstring="""This arguments shows more info about user""")

    # nickname
    NICKNAME = Argument(long='nickname',
                        short='n',
                        docstring="""This arguments allows user to specify nickname
                        by his own""")

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
                           the admin from the name of current user. If in change
                           task, then it specifies the project within task is 
                           placed""")
    # TODO: maybe delete creator id to have more flexible rights (but it's hard)

    # show projects
    SHOW_PROJECTS = Argument(long='showprojects',
                             short='sp',
                             docstring="""Show all available projects to the 
                             current person""")

    # project members
    MEMBERS = Argument(long='members',
                       short='m',
                       docstring="""This argument specify id's of the users
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
                        later. Can be: 0 - min, 1 - low, 2 - medium, 3 - high, 4
                         - max.""")

    # task time
    TIME = Argument(long='time',
                    short='t',
                    docstring="""task\'s time, can be changed later. If not 
                    passed, then time is not determent. Format is 
                    YYYY-MM-DD HH:MM:SS or simple HH:MM:SS""")

    # task status
    STATUS = Argument(long='status',
                      short='s',
                      docstring="""task\'s status, that can be changed later.
                      Can be: 0 - expired, 1 - cancelled, 2 - in_progress, 3 - 
                      done.""")

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

    # task period
    PERIOD = Argument(long='period',
                      short='e',
                      docstring="""task\'s period. It can be set up in hours.
                      Note that if it used with planner, then period 
                      automatically will became equals to 7 days ignoring the
                      fact of this period""")

    # task period
    PLANNER = Argument(long='planner',
                       short='l',
                       docstring="""task\'s planner. This argument is a string
                       in format of sequence of numbers from 1 to 7. This 
                       argument suppress period argument. It gives auto 7 day
                       period to the task""")

    # task receiver
    RECEIVER = Argument(long='receiver',
                        short='c',
                        docstring="""task\'s receiver, i e user's id, whom
                        will be the task's executioner in the project.""")

    """
    Also project argument
    """
    # current user
    WHO_AM_I = Argument(long='whoami',
                        short='w',
                        docstring="""show the info about logged user""")

    # remove task
    REMOVE_TASK = Argument(long='removetask',
                           short='rmt',
                           docstring="""Remove task from the database by id""")

    # change task
    CHANGE_TASK = Argument(long='changetask',
                           short='ct',
                           docstring="""Changing one of the possible values to 
                           the task by it's id and optional parameters""")

    # remove project
    REMOVE_PROJECT = Argument(long='removeproject',
                              short='rmp',
                              docstring="""Remove project from the database by 
                              id""")

    # change project
    CHANGE_PROJECT = Argument(long='changeproject',
                              short='cp',
                              docstring="""Changing one of the possible values 
                              to the project by it's id and optional parameters
                              """)

    # project's title
    TITLE = Argument(long='title',
                     short='t',
                     docstring="""This argument can be used to change project's
                     title""")

    # remove user
    REMOVE_USER = Argument(long='removeuser',
                           short='rmu',
                           docstring="""Remove user or something related to 
                           the user from the database""")

    # show tasks
    SHOW_TASKS = Argument(long='showtasks',
                          short='st',
                          docstring="""Show all available tasks to the current 
                          person, including tasks where he is a creator. To 
                          show some type of sorted tasks, see the special 
                          parser syntax""")

    # show users
    SHOW_USERS = Argument(long='showusers',
                          short='su',
                          docstring="""Show all users by filter (just user 
                          substring)""")

    # show tasks filter
    FILTER = Argument(long='filter',
                      short='f',
                      docstring="""Filter all available tasks by one 
                      expression with own syntax""")

    # TODO: filter will replace this argument?
    ALL_TASKS = Argument(long='all',
                         short='a',
                         docstring="""If this flag is set, we will show all 
                         tasks, with the project user's tasks""")

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
    global app_controller, user_controller
    user_controller = UserController(db_file=config.USERS_DATABASE_PATH)
    user = UserController.load_user()
    app_controller = AppController(db_file=config.DATABASE_PATH,
                                   uid=user.uid)

    parser = argparse.ArgumentParser(prog='time_candle')

    # root_args is the main command arguments, that defines next action
    root_args = parser.add_subparsers(dest=_Args.action.long,
                                      help='sub-command help')

    # for each command initialize parser and it's specific arguments
    _init_add_user_parser(root_args)
    _init_add_task_parser(root_args)
    _init_login_parser(root_args)
    _init_add_project_parser(root_args)
    _init_change_task_parser(root_args)
    _init_remove_task_parser(root_args)
    _init_show_tasks_parser(root_args)
    _init_remove_project_parser(root_args)
    _init_show_users_parser(root_args)
    _init_change_project_parser(root_args)
    _init_remove_user_parser(root_args)
    _init_whoami_parser(root_args)
    _init_show_projects_parser(root_args)

    # simple clear log arg
    root_args.add_parser(_Args.CLEAR_LOG.long,
                         help=_Args.CLEAR_LOG.docstring)

    # simple logout arg
    root_args.add_parser(_Args.LOGOUT.long,
                         help=_Args.LOGOUT.docstring)

    # easter egg
    root_args.add_parser('watch')

    parsed = parser.parse_args()
    logger.debug(parsed)

    try:
        # try to process each command
        if parsed.action == _Args.ADD_USER.long:
            _process_add_user(parsed)

        elif parsed.action == _Args.REMOVE_USER.long:
            _process_remove_user(parsed)

        elif parsed.action == _Args.LOGIN.long:
            _process_login(parsed)

        elif parsed.action == _Args.ADD_TASK.long:
            _process_add_task(parsed)

        elif parsed.action == _Args.CLEAR_LOG.long:
            open(config.LOG_PATH, 'w').close()
            logger.info('log has been cleared')

        elif parsed.action == _Args.LOGOUT.long:
            _process_logout()

        elif parsed.action == _Args.ADD_PROJECT.long:
            _process_add_project(parsed)

        elif parsed.action == _Args.REMOVE_PROJECT.long:
            _process_remove_project(parsed)

        elif parsed.action == _Args.CHANGE_PROJECT.long:
            _process_change_project(parsed)

        elif parsed.action == _Args.CHANGE_TASK.long:
            _process_change_task(parsed)

        elif parsed.action == _Args.REMOVE_TASK.long:
            _process_remove_task(parsed)

        elif parsed.action == _Args.SHOW_TASKS.long:
            _process_show_tasks(parsed)

        elif parsed.action == _Args.SHOW_USERS.long:
            _process_show_users(parsed)

        elif parsed.action == _Args.SHOW_PROJECTS.long:
            _process_show_projects(parsed)

        elif parsed.action == _Args.WHO_AM_I.long:
            _process_whoami()

        elif parsed.action == 'watch':
            print_functions.watch()

    except (AppException, AuthenticationError) as e:
        if config.VERBOSE:
            logger.exception('Error occured:')
            print('Message text: {}'.format(e.errors.value))
        else:
            print(e.message.format(e.errors.value))


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

    user.add_argument(_Args.prefix().MAIL.long,
                      _Args.prefix().MAIL.short,
                      help=_Args.MAIL.docstring,
                      nargs=1,
                      default=[None])

    user.add_argument(_Args.prefix().NICKNAME.long,
                      _Args.prefix().NICKNAME.short,
                      help=_Args.NICKNAME.docstring,
                      nargs=1,
                      default=[None])

    user.add_argument(_Args.prefix().ABOUT.long,
                      _Args.prefix().ABOUT.short,
                      help=_Args.ABOUT.docstring,
                      nargs=1,
                      default=[''])


def _init_remove_user_parser(root_args):
    # create new parser for removeuser command
    user = root_args.add_parser(_Args.REMOVE_USER.long,
                                help=_Args.REMOVE_USER.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')

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
                      type=int,
                      default=[None])

    task.add_argument(_Args.prefix().STATUS.long,
                      _Args.prefix().STATUS.short,
                      help=_Args.STATUS.docstring,
                      nargs=1,
                      type=int,
                      default=[None])

    task.add_argument(_Args.prefix().TIME.long,
                      _Args.prefix().TIME.short,
                      help=_Args.TIME.docstring,
                      nargs=1,
                      default=[None])

    task.add_argument(_Args.prefix().PARENT.long,
                      _Args.prefix().PARENT.short,
                      help=_Args.PARENT.docstring,
                      type=int,
                      nargs=1,
                      default=[None])

    task.add_argument(_Args.prefix().PROJECT.long,
                      _Args.prefix().PROJECT.short,
                      help=_Args.PROJECT.docstring,
                      default=[None],
                      nargs=1)

    task.add_argument(_Args.prefix().COMMENT.long,
                      _Args.prefix().COMMENT.short,
                      help=_Args.COMMENT.docstring,
                      default=[''],
                      nargs=1)

    task.add_argument(_Args.prefix().PERIOD.long,
                      _Args.prefix().PERIOD.short,
                      help=_Args.PERIOD.docstring,
                      default=[None],
                      type=int,
                      nargs=1)

    task.add_argument(_Args.prefix().RECEIVER.long,
                      _Args.prefix().RECEIVER.short,
                      help=_Args.RECEIVER.docstring,
                      default=[None],
                      type=int,
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
                      nargs=1,
                      type=int,
                      default=[None])

    task.add_argument(_Args.prefix().STATUS.long,
                      _Args.prefix().STATUS.short,
                      help=_Args.STATUS.docstring,
                      nargs=1,
                      type=int,
                      default=[None])

    task.add_argument(_Args.prefix().TIME.long,
                      _Args.prefix().TIME.short,
                      help=_Args.TIME.docstring,
                      nargs=1,
                      default=[None])

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


def _init_whoami_parser(root_args):
    # create new parser for whoami command
    root_args.add_parser(_Args.WHO_AM_I.long,
                         help=_Args.WHO_AM_I.docstring)


def _init_show_tasks_parser(root_args):
    # create new parser for login command
    show = root_args.add_parser(_Args.SHOW_TASKS.long,
                                help=_Args.SHOW_TASKS.docstring)

    show.add_argument(_Args.prefix().FILTER.long,
                      _Args.prefix().FILTER.short,
                      help=_Args.FILTER.docstring,
                      nargs=1,
                      default=[''])


def _init_show_users_parser(root_args):
    # create new parser for login command
    show = root_args.add_parser(_Args.SHOW_USERS.long,
                                help=_Args.SHOW_USERS.docstring)

    show.add_argument(_Args.prefix().FILTER.long,
                      _Args.prefix().FILTER.short,
                      help=_Args.FILTER.docstring,
                      nargs=1,
                      default=[''])

    show.add_argument(_Args.prefix().PROJECT.long,
                      _Args.prefix().PROJECT.short,
                      help=_Args.PROJECT.docstring,
                      type=int,
                      nargs=1,
                      default=[None])


def _init_show_projects_parser(root_args):
    # create new parser for login command
    show = root_args.add_parser(_Args.SHOW_PROJECTS.long,
                                help=_Args.SHOW_PROJECTS.docstring)

    show.add_argument(_Args.prefix().FILTER.long,
                      _Args.prefix().FILTER.short,
                      help=_Args.FILTER.docstring,
                      nargs=1,
                      default=[''])


def _init_change_project_parser(root_args):
    # create new parser for changeproject command
    project = root_args.add_parser(_Args.CHANGE_PROJECT.long,
                                   help=_Args.CHANGE_PROJECT.docstring)

    project.add_argument('id', help='project\'s id in database')
    project.add_argument(_Args.prefix().TITLE.long,
                         _Args.prefix().TITLE.short,
                         help=_Args.TITLE.docstring,
                         nargs=1,
                         default=[None])

    project.add_argument(_Args.prefix().DESCRIPTION.long,
                         _Args.prefix().DESCRIPTION.short,
                         help=_Args.DESCRIPTION.docstring,
                         nargs=1,
                         default=[None])


def _init_remove_project_parser(root_args):
    # create new parser for removeproject command
    project = root_args.add_parser(_Args.REMOVE_PROJECT.long,
                                   help=_Args.REMOVE_PROJECT.docstring)

    project.add_argument('id', help='project\'s id in database')


# Process parsed arguments
def _process_login(parsed_args):
    logger.debug('login')
    if user_controller.log_in(parsed_args.login, parsed_args.password):
        print('user %s logged' % parsed_args.login)
    else:
        print('user %s is not logged' % parsed_args.login)


def _process_add_task(parsed_args):
    logger.debug('add_task')
    user_controller.authenticate()

    app_controller.add_task(parsed_args.title,
                            parsed_args.priority[0],
                            parsed_args.status[0],
                            parsed_args.time[0],
                            parsed_args.parent[0],
                            parsed_args.comment[0],
                            parsed_args.project[0],
                            parsed_args.receiver[0],
                            parsed_args.period[0])
    print('task %s added' % parsed_args.title)


def _process_change_task(parsed_args):
    logger.debug('change_task')
    user_controller.authenticate()

    app_controller.change_task(parsed_args.id,
                               parsed_args.priority[0],
                               parsed_args.status[0],
                               parsed_args.time[0],
                               parsed_args.comment[0])
    print('task %s changed' % parsed_args.id)


def _process_remove_task(parsed_args):
    logger.debug('remove_task')
    user_controller.authenticate()
    app_controller.remove_task(parsed_args.id)
    print('task %s removed' % parsed_args.id)


def _process_logout():
    user_controller.logout()
    print('successfully logged out')


def _process_add_user(parsed_args):
    logger.debug('add_user')
    if parsed_args.project is None:
        if parsed_args.password == '':
            raise ValueError('You must specify the password!')

        external_id = user_controller.add_user(parsed_args.login,
                                               parsed_args.password,
                                               parsed_args.mail[0])
        app_controller.add_user(parsed_args.login,
                                external_id,
                                parsed_args.nickname[0],
                                parsed_args.about[0])

        print('user %s added' % parsed_args.login)

    else:
        app_controller.add_user_to_project(
            parsed_args.login, parsed_args.project[0])
        print('user %s added to project %s' %
              (parsed_args.login, parsed_args.project[0]))


def _process_add_project(parsed_args):
    logger.debug('add_project')
    user_controller.authenticate()
    app_controller.add_project(parsed_args.title,
                               parsed_args.description[0],
                               parsed_args.members)
    print('project %s added' % parsed_args.title)


def _process_show_tasks(parsed_args):
    user_controller.authenticate()
    tasks = app_controller.get_tasks(parsed_args.filter[0])
    print_functions.print_tasks(tasks)


def _process_show_users(parsed_args):
    if parsed_args.project[0] is None:
        users = app_controller.get_users_by_nickname(parsed_args.filter[0])
    else:
        user_controller.authenticate()
        users = app_controller.get_users(parsed_args.project[0])

    print_functions.print_users(users)


def _process_show_projects(parsed_args):
    user_controller.authenticate()
    projects = app_controller.get_projects(parsed_args.filter[0])
    print_functions.print_projects(projects)


def _process_whoami():
    uid = user_controller.get_current_user().uid
    user = app_controller.get_user(uid)
    print_functions.cow_print_user(user)


def _process_change_project(parsed_args):
    user_controller.authenticate()
    app_controller.change_project(parsed_args.id,
                                  parsed_args.title[0],
                                  parsed_args.description[0])
    print('project %s changed' % parsed_args.id)


def _process_remove_project(parsed_args):
    user_controller.authenticate()
    app_controller.remove_project(parsed_args.id)
    print('project %s removed' % parsed_args.id)


def _process_remove_user(parsed_args):
    if parsed_args.project is not None:
        app_controller.remove_user_from_project(
            parsed_args.login, parsed_args.project)
        print('user %s removed from %s project' %
              (parsed_args.login, parsed_args.id))
    else:
        print('nothing to expect')
