#!/usr/bin/env python3
import commands_parser
import app_logger
import tokenizer
import storage.task_adapter as ta
from enums.priority import Priority
from storage.adapter_classes import Filter
from pprint import pprint
import config_parser
# TODO: cut down lower part of the code from this module


def main():
    """
    usr = config_parser.run_config()['user']
    usr.say_hi()
    """
    app_logger.custom_logger('root').info('Entering the program.')
    fil = ta.TaskFilter()
    fil.priority(Priority.HIGH, ta.TaskFilter.OP_GREATER_OR_EQUALS,
                 op=Filter.OP_AND)
    fil.priority(Priority.MAX, ta.TaskFilter.OP_LESS,
                 op=Filter.OP_AND)
    print(ta.get_by_filter(fil))
    commands_parser.run()

    with open('tokenizer.py', 'r') as myfile:
        data = myfile.read().replace('\n', '')

    print(tokenizer.decistmt("data:'name', 'field' ; this_is_sparta:'huh', 1 > 2"))

    app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
