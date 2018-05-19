#!/usr/bin/env python3
import commands_parser
import app_logger
from model.session_control import start_session
# TODO: cut down lower part of the code from this module


def main():
    """
    usr = config_parser.run_config()['user']
    usr.say_hi()
    """
    app_logger.custom_logger('root').info('Entering the program.')
    start_session('dev')
    """
    fil = ta.TaskFilter()
    fil.priority(Priority.LOW, ta.TaskFilter.OP_GREATER_OR_EQUALS,
                 op=Filter.OP_AND)

    print(ta.get_by_filter(fil))
    fil2 = ta.TaskFilter()
    fil2.priority(Priority.MAX, ta.TaskFilter.OP_LESS,
                  op=Filter.OP_AND)
    print(ta.get_by_filter(fil2))
    print(ta.get_by_filter(fil & fil2))

    fil = ua.UserFilter()
    fil.login_substring('n')
    print(ua.get_users_by_filter(fil))
    """

    commands_parser.run()

    # pprint(tokenizer.parse_string("data:'name', 'field' ; this_is_sparta:'huh', 1.2 > 2"))

    app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
