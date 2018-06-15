"""
This module is module for most validations some inner values and conversions.
Also it has some other mini helper functions.
"""
import re
import time_candle.exceptions.validation_exceptions as v_e


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


def check_comment(comment):
    """
    Checks comment length and other parameters
    :param comment: Comment string
    :return: None
    """
    if len(comment) > 255:
        raise v_e.InvalidCommentError(v_e.CommentMessages.INVALID_COMMENT)


def check_title(title):
    """
    Checks comment length and other parameters
    :param title: Title string
    :return: None
    """
    if len(title) > 100 or len(title) < 1:
        raise v_e.InvalidTitleError(v_e.TitleMessages.INVALID_TITLE)
