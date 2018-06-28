#!/usr/bin/env python3
import time_candle.app_logger
from tc_cli import commands_parser
import sys


def main():
    time_candle.app_logger.custom_logger('root').info('Entering the program.')

    status = commands_parser.run()

    time_candle.app_logger.custom_logger('root').info('Leaving the program.')

    sys.exit(status)


if __name__ == "__main__":
    main()
