import logging
import logging.config


_loggers = []


def custom_logger(logger_name):
    """
    This function returns selected from the logging.conf logger to write more
    stylish and useful messages in our app
    :param logger_name: name of the logger in the logging.conf
    :type logger_name: String
    :return:
    """
    global _loggers

    if not _loggers:
        logging.config.fileConfig('logging.conf')

    if logger_name not in [lg.name for lg in _loggers]:
        logger = logging.getLogger(logger_name)
        _loggers.append(logger)

    else:
        logger = next((lg for lg in _loggers if lg.name == logger_name), None)

    return logger
