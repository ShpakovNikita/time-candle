#!/usr/bin/env python3
import commands_parser
import app_logger
import model.tokenizer
from model.session_control import start_session
# TODO: cut down lower part of the code from this module


def main():
    app_logger.custom_logger('root').info('Entering the program.')
    start_session('dev')

    commands_parser.run()
    model.tokenizer.parse_string('')
    # pprint(tokenizer.parse_string("data:'name', 'field' ; this_is_sparta:'huh', 1.2 > 2"))

    app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
