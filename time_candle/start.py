#!/usr/bin/env python3
from console import commands_parser
import app_logger
from model.session_control import start_session


def main():
    app_logger.custom_logger('root').info('Entering the program.')

    start_session('dev')
    commands_parser.run()

    app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
