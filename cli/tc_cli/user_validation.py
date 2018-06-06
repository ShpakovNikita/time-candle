import re
import time_candle.exceptions.validation_exceptions as v_e
"""
This module is module for most validations some inner values and conversions. 
Also it has some other mini helper functions.
"""


def check_password(password):
    """
    Validates typed password.
    :param password: String
    :return: None
    """
    raw_password_pattern = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    if re.match(raw_password_pattern, password) is None:
        raise v_e.InvalidPasswordError(v_e.PasswordMessages.INVALID_PASSWORD)


def check_mail(mail):
    """
    Validates typed email and raises exception if it doesn't match to the regex
    pattern. More about this regex you can read at http://emailregex.com/
    :param mail: The user mail
    :type mail: String
    :return: None
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
        raise v_e.InvalidMailError(v_e.MailMessages.INVALID_MAIL)


def check_login(login):
    """
    Validates typed login.
    :param login: String
    :return: None
    """
    raw_login_pattern = (r"^(?=.{4,15}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<!"
                         r"[_.])$")

    if re.match(raw_login_pattern, login) is None:
        raise v_e.InvalidNameError(v_e.NameMessages.INVALID_LOGIN)


def check_name(name):
    """
    Validates typed login or nickname.
    :param name: String
    :return: None
    """
    raw_name_pattern = (r"^(?=.{4,15}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<!["
                        r"_.])$")

    if re.match(raw_name_pattern, name) is None:
        raise v_e.InvalidNameError(v_e.NameMessages.INVALID_NICKNAME)
