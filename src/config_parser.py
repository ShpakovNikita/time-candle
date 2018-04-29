import configparser
from main_instances.user import User
import sql_shell.exceptions

CONFIG_NAME = 'config.ini'


def run_config():
    """
    This function returns dictionary with initialized instances from the config
    file.
    :return: dict in the following format:
    {
        'user':User
    }
    """
    # TODO: Check if user is in database and password is correct
    config = configparser.ConfigParser()
    config.read(CONFIG_NAME)

    # config_dict contains parsed dictionary from config file, but with
    # initialized instances
    config_dict = {}
    try:
        user_name = config['user']['name']
        password = config['user']['password']

        # Create user by it's name and password. If it exists, we will get it
        # from database
        config_dict['user'] = User.create_user(user_name, password)
        return config_dict

    except KeyError:
        raise sql_shell.exceptions.InvalidLoginException


def write_config(user):
    # TODO: Check if user is in database and password is correct
    config = configparser.ConfigParser()
    config['user'] = user.login
    config['password'] = user.password
