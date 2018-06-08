#!/usr/bin/env python3
import os
import console.settings as config
import time_candle.app_logger

if not os.path.exists(config.BASE_DIR):
    os.makedirs(config.BASE_DIR)
time_candle.app_logger.setup_logging(
    enabled=config.ENABLED,
    log_conf=config.LOG_CONF_PATH)

from console import commands_parser


def main():
    time_candle.app_logger.custom_logger('root').info('Entering the program.')

    commands_parser.run(config.MODE)

    time_candle.app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
