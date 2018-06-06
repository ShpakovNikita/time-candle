import logging
import logging.config
import time_candle.exceptions as e
from configparser import MissingSectionHeaderError


_loggers = []
_ENABLED = True
_LOG_CONF = 'logging.conf'


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
        _loggers.append(logger)

    else:
        logger = next((lg for lg in _loggers if lg.name == logger_name), None)

    if _ENABLED:
        logger.disabled = False
    else:
        logger.disabled = True

    return logger


def setup_logging(enabled=True, log_conf=_LOG_CONF):
    global _ENABLED, _LOG_CONF
    _ENABLED = enabled
    _LOG_CONF = log_conf
