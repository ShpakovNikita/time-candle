import logging
import logging.config
from configparser import MissingSectionHeaderError
import sys


_loggers = []
_ENABLED = True
_LOG_CONF = 'logging.conf'
_LOG_FILE = None
_LOG_LEVEL = logging.DEBUG

_DEFAULT_FORMATTER = '[%(asctime)s] [%(name)s]:%(levelname)s: %(message)s'
_DEFAULT_TIME = '%Y-%m-%d %H:%M:%S'


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
        try:
            logging.config.fileConfig(_LOG_CONF)
        except (MissingSectionHeaderError, KeyError):
            logger = logging.getLogger('nani')
            logger.disabled = True
            return logger

    if logger_name not in [lg.name for lg in _loggers]:
        logger = logging.getLogger(logger_name)

        if _LOG_FILE:
            formatter = logging.Formatter(_DEFAULT_FORMATTER, _DEFAULT_TIME)
            fh = logging.FileHandler(_LOG_FILE)
            fh.setFormatter(formatter)
            fh.setLevel(_LOG_LEVEL)
            logger.addHandler(fh)

        _loggers.append(logger)

    else:
        logger = next((lg for lg in _loggers if lg.name == logger_name), None)

    if not _ENABLED:
        logging.disable(logging.CRITICAL)

    return logger


def setup_logging(enabled=True,
                  log_conf=_LOG_CONF,
                  log_path=_LOG_FILE,
                  time_format=_DEFAULT_TIME,
                  logging_level=_LOG_LEVEL):
    global _ENABLED, _LOG_CONF, _LOG_FILE, _DEFAULT_TIME, _LOG_LEVEL
    _ENABLED = enabled
    _LOG_CONF = log_conf
    _LOG_FILE = log_path
    _DEFAULT_TIME = time_format
    _LOG_LEVEL = logging_level
