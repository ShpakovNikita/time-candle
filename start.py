#!/usr/bin/env python3
from console import commands_parser
import time_candle.app_logger


def main():
    time_candle.app_logger.custom_logger('root').info('Entering the program.')

    commands_parser.run('dev')

    time_candle.app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()