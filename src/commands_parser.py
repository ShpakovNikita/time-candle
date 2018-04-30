import argparse
from collections import namedtuple
import commands


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

    # login tree arguments
    LOGIN = Argument(long='login',
                     short='l',
                     docstring="""This argument make next sessions from the 
                     logged users, i. e. add tasks, show their tasks etc.""")

    # add_task tree arguments
    ADD_TASK = Argument(long='addtask',
                        short='t',
                        docstring="""This argument adds a new task to the user 
                        or project""")

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
    :return: Nothing
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

    parsed = parser.parse_args()
    print(parsed)

    # try to process each command
    if parsed.action == _Args.ADD_USER.long:
        print('add_user')
        commands.add_user(parsed.login, parsed.password)

    if parsed.action == _Args.LOGIN.long:
        print('login')
        commands.log_in(parsed.login, parsed.password)

    # _test_help()


def _test_help():
    # Just for tip
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG', prefix_chars='--')
    # root_subparsers = parser.add_subparsers(dest=ParseArguments.action)
    parser.add_argument('--foo', action='store_true', help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    parser_a = subparsers.add_parser('a', help='a help')
    parser_a.add_argument('--bar', type=int, help='bar help')

    # create the parser for the "b" command
    parser_b = subparsers.add_parser('b', help='b help')
    parser_b.add_argument('baz', choices='XYZ', help='baz help')

    # parse some argument lists
    print(parser.parse_args(['--foo', 'a', '--bar', '12']))

    print(parser.parse_args(['--foo', 'b', 'Z']))


"""
The functions below are private. So do not use it int any cases outside this 
commands parser module.
"""


def _init_add_user_parser(root_args):
    # create new parser for adduser command
    user = root_args.add_parser(_Args.ADD_USER.long,
                                help=_Args.ADD_USER.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')
    user.add_argument('password', help='user password')


def _init_add_task_parser(root_args):
    # create new parser for addtask command
    root_args.add_parser(_Args.ADD_TASK.long, help=_Args.ADD_TASK.docstring)


def _init_login_parser(root_args):
    # create new parser for login command
    user = root_args.add_parser(_Args.LOGIN.long,
                                help=_Args.LOGIN.docstring)

    # define two positional arguments login password
    user.add_argument('login', help='user login')
    user.add_argument('password', help='user password')
