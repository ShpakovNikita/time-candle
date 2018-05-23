import logging
import logging.config
from os import path
from pathlib import Path
import platform


_loggers = []
LOG_FILENAME = 'config.log'

if platform.system() == 'Linux':
    CONFIG_PATH = path.join(str(Path.home()), 'logging.conf')
else:
    CONFIG_PATH = path.join(
        path.dirname(path.abspath(__file__)), 'logging.conf')


def custom_logger(logger_name):
    """
    This function returns selected from the logging.conf logger to write more
    stylish and useful messages in our app
    :param logger_name: name of the logger in the logging.conf
    :type logger_name: String
    :return: Logger, in which you may call all needed logging module functions
    """
    global _loggers

    if not _loggers:
        logging.config.fileConfig(CONFIG_PATH)

    if logger_name not in [lg.name for lg in _loggers]:
        logger = logging.getLogger(logger_name)
        _loggers.append(logger)

    else:
        logger = next((lg for lg in _loggers if lg.name == logger_name), None)

    return logger
