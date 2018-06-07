#!/usr/bin/env python3
from . import settings as config
import time_candle.app_logger
from . import commands_parser


def main():
    time_candle.app_logger.custom_logger('root').info('Entering the program.')

    commands_parser.run(config.MODE)

    time_candle.app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
