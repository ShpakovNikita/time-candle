import config_parser
from main_instances.user import User
import os
from storage import *
import storage.adapter_classes
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case and conversion to the primary entities.
"""


def log_in(login, password):
    """
    Writes current user to the config.ini
    :param login: string
    :param password: string
    :return: Nothing
    """
    # TODO: Yes, it is protected member and it is bad to use it
    storage.adapter_classes._test_login(login, password)


def add_user(login, password):
    # TODO: Yes, it is protected member and it is bad to use it
    storage.adapter_classes._test_add_user(login, password)
    pass


def add_task():
    _login().say_hi()
    pass


def _login():
    """
    Returns loaded user to make some actions from it's name. User will be
    initialized from config file.
    :return: User
    """

    return config_parser.run_config()['user']
