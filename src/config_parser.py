import configparser
from main_instances.user import User
import sql_shell.exceptions

CONFIG_NAME = 'config.ini'


def run_config():
    # TODO: Check if user is in database and password is correct
    config = configparser.ConfigParser()
    config.read(CONFIG_NAME)
    config_dict = {}
    try:
        user_name = config['user']['name']
        config_dict['user'] = User.create_user(user_name)
        return config_dict

    except KeyError:
        raise sql_shell.exceptions.InvalidLoginException


def write_config(user):
    # TODO: Check if user is in database and password is correct
    config = configparser.ConfigParser()
    config['user'] = user.login
    config['password'] = user.password
