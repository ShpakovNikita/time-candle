import time_candle.exceptions.validation_exceptions as v_e
"""
This module is module for most validations some inner values and conversions. 
Also it has some other mini helper functions.
"""


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
