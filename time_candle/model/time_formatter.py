import re
from datetime import datetime, time
import time_candle.exceptions.model_exceptions as m_e
from time_candle.model import logger
"""
All date logic is placed in this module.
"""


# We will be storing data only from 1970 year
epoch = datetime.utcfromtimestamp(1970)

# One hour error that are got from the epoch timestamp
error = 60 * 60 * 1000


# Get time_stamp func
def time_delta(milliseconds,
               now=None):
    """
    This function gets timestamp from passed time and now time (now can be
    specified for some tests)
    :param milliseconds: time in milliseconds
    :param now: now time in milliseconds
    :return: Int (our timestamp)
    """
    if now is None:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        now = get_milliseconds(now)

    return milliseconds - now


def days_to_milliseconds(days):
    """
    This function get's days in milliseconds.
    :param days: Int days
    :return: Int (time in milliseconds)
    """
    # of course it is 24 * 60 * 60 * 1000
    return days * 5 * 1000


def milliseconds_to_days(milliseconds):
    """
    This function converts milliseconds to days
    :param milliseconds:
    :return:
    """
    return int(milliseconds / 5 / 1000)


def get_next_deadline(period, start, now=None):
    """
    This function calculates next deadline according to the start and now time
    :param period: period in milliseconds
    :param start: start point in milliseconds
    :param now: now time in milliseconds
    :return: Int (next deadline)
    """
    if now is None:
        now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        now = get_milliseconds(now)

    if now < start:
        return start

    return start + ((now - start) // period + 1) * period


def get_now_milliseconds():
    """
    This functions returns now datetime in milliseconds with epoch calculations
    :return: Int
    """
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    return get_milliseconds(now)


# This format is given only for example, you should specify it from the call
def get_milliseconds(formatted_time):
    """
    This function returns time in milliseconds according to the given formatted
    time
    :param formatted_time: Time in following format of date_format
    (%Y-%m-%d %H:%M:%S)
    :type formatted_time: String
    :return: Int
    """

    date_format = '%Y-%m-%d %H:%M:%S'
    logger.debug('passed time %s' % formatted_time)

    try:
        date_time = datetime.strptime(_time_get_formatted(formatted_time),
                                      date_format)
        logger.debug('date converted')

        # Note that here we are subtracting 1970's to define them as lower point
        final_time = (date_time - epoch).total_seconds() * 1000 - error
        if final_time < 0:
            raise m_e.\
                InvalidArgumentFormat('date must be from 1970\'s')

        return int(final_time)
    except ValueError:
        logger.warning('the date must be ' + date_format)
        msg = "Not a valid date: '{0}'.".format(formatted_time)
        raise m_e.InvalidArgumentFormat(msg)


def _time_get_formatted(formatted_time):
    """
    This function returns formatted_time, but with the now's date if the date
    is not pointed
    :param formatted_time: string of formatted time
    :type formatted_time: String
    :return: String of format %Y-%m-%d %H:%M:%S to the strptime function
    """
    long_pattern = r'\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}'
    short_pattern = r'\d{1,2}:\d{1,2}:\d{1,2}'
    if re.match(long_pattern, formatted_time):
        logger.debug('date matched long pattern')
        return formatted_time
    elif re.match(short_pattern, formatted_time):
        logger.debug('date matched short pattern')
        date_string = datetime.strftime(datetime.now(), '%Y-%m-%d')
        return date_string + ' ' + formatted_time
    else:
        logger.warning('the date must be %Y-%m-%d or %Y-%m-%d %H:%M:%S')
        msg = "Not a valid date: '{0}'.".format(formatted_time)
        raise m_e.InvalidArgumentFormat(msg)


def get_datetime(milliseconds_time):
    """
    This function converts given data from database to the normal datetime class
    according to the epoch variable
    :param milliseconds_time: Time in milliseconds
    :type milliseconds_time: Int
    :return: DateTime
    """

    # we also have to add epoch to convert it to a normal datetime due to we
    # store date time in milliseconds
    final_time = datetime.fromtimestamp((milliseconds_time +
                                         epoch.timestamp() * 1000) / 1000)
    return final_time


def date_to_string(date_time):
    """
    This function converts our date_time to the application format of time, i e
    %Y-%m-%d %H:%M:%S
    :param date_time: datetime instance
    :return: String
    """
    return datetime.strftime(date_time, '%Y-%m-%d %H:%M:%S')


def milliseconds_to_string(milliseconds):
    """
    This function converts milliseconds to formatted string
    :param milliseconds: Int time
    :return: String
    """
    date_time = get_datetime(milliseconds)
    return date_to_string(date_time)
