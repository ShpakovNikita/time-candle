import config_parser
from main_instances.user import User
import os
from adapters import *
import adapters.adapter_classes
"""
This is commands module. Commands from argparse and django will go to this 
module and it will help to separate argparser from the model. In this module 
also we have a validation for each case. 
"""


def log_in(login, password):
    """
    Writes current user to the config.ini
    :param login: string
    :param password: string
    :return: Nothing
    """
    # TODO: Yes, it is protected member and it is bad to use it
    adapters.adapter_classes._test_login(login, password)


def add_user(login, password):
    # TODO: Yes, it is protected member and it is bad to use it
    adapters.adapter_classes._test_add_user(login, password)
    pass


def add_task():
    pass
