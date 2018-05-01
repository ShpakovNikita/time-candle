import re
from datetime import datetime, date, time


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


def get_milliseconds(formatted_time):
    """
    This function returns time in milliseconds according to the given formatted
    time
    :param formatted_time: Time in following format: YYYY-MM-DD HH:MM:SS
    :type formatted_time: String
    :return: Int
    """

    # TODO: Real validator
    try:
        return datetime.strptime(formatted_time, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(formatted_time)
        raise ValueError(msg)
        # TODO: own exception
