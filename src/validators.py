import re
from datetime import datetime, date, time
import app_logger
import exceptions.exceptions
"""
This module is module for most validations some inner values and conversions. 
Also it has some other mini helper functions.
"""
# We will be storing data only from 1970 year
epoch = datetime.utcfromtimestamp(1970)


def check_mail(mail):
    """
    Validates typed email and raises exception if it doesn't match to the regex
    pattern. More about this regex you can read at http://emailregex.com/
    :param mail: The user mail
    :type mail: String
    :return: Nothing
    """
    raw_mail_pattern = (
                        r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/="
                        r"?^_`{|}~-]+)*|(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-"
                        r"\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*)@(?:("
                        r"?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0"
                        r"-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9"
                        r"][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?"
                        r"|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x2"
                        r"1-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
                        )

    if re.match(raw_mail_pattern, mail) is None:
        raise ValueError("Please, input correct email")


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
    app_logger.custom_logger('model').debug('passed time %s' % formatted_time)

    try:
        date_time = datetime.strptime(_time_get_formatted(formatted_time),
                                      date_format)
        app_logger.custom_logger('model').debug('date converted')

        # Note that here we are subtracting 1970's to define them as lower point
        final_time = (date_time - epoch).total_seconds() * 1000
        if final_time < 0:
            raise exceptions.exceptions.InvalidArgumentFormat('date must be '
                                                              'from 1970\'s')

        return int(final_time)
    except ValueError:
        app_logger.custom_logger('model').warning('the date must be '
                                                  + date_format)
        msg = "Not a valid date: '{0}'.".format(formatted_time)
        raise exceptions.exceptions.InvalidArgumentFormat(msg)


def _time_get_formatted(formatted_time):
    """
    This function returns formatted_time, but with the now's date if the date
    is not pointed
    :param formatted_time: string of formatted time
    :type formatted_time: String
    :return: String of format %Y-%m-%d %H:%M:%S to the strptime function
    """
    long_pattern = r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})'
    short_pattern = r'(\d{2}):(\d{2}):(\d{2})'
    if re.match(long_pattern, formatted_time):
        app_logger.custom_logger('model').debug('date matched long pattern')
        return formatted_time
    elif re.match(short_pattern, formatted_time):
        app_logger.custom_logger('model').debug('date matched short pattern')
        date_string = datetime.strftime(datetime.now(), '%Y-%m-%d')
        return date_string + ' ' + formatted_time
    else:
        app_logger.custom_logger('model').warning('the date must be '
                                                  '%Y-%m-%d or %Y-%m-%d '
                                                  '%H:%M:%S')
        msg = "Not a valid date: '{0}'.".format(formatted_time)
        raise exceptions.exceptions.InvalidArgumentFormat(msg)


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


def not_null_do_action(arg1, arg2, action):
    # if the first argument is not none then return action of two args, else
    # return first arg
    if arg1 is not None:
        return action(arg1, arg2)
    else:
        return arg1
