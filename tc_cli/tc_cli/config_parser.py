import configparser
import time_candle.exceptions.model_exceptions as m_e
from tc_cli.user import User
from tc_cli.user_adapter import UserAdapter
from tc_cli import exceptions as auth_e
import os


CONFIG_NAME = 'config.ini'


def run_config():
    """
    This function returns dictionary with initialized instances from the config
    file.
    :return: dict in the following format:
    {
        'user':User or user_field
    }
    """
    config = configparser.ConfigParser()
    config.read(CONFIG_NAME)

    # config_dict contains parsed dictionary from config file, but with
    # initialized instances
    config_dict = {}
    try:
        login = config['user']['name']
        password = config['user']['password']

        # Create user by it's name and password. If it exists, we will get it
        # from database
        user_field = type('user_field', (), {'uid': None,
                                             'login': 'Sans the Skeleton',
                                             'mail': None,
                                             'password': ''})
        try:
            config_dict['user'] = UserAdapter.authenticate(login, password)

        except auth_e.InvalidPasswordError:
            config_dict['user'] = user_field()

        except auth_e.InvalidLoginError:
            config_dict['user'] = user_field()
        return config_dict

    except KeyError:
        raise m_e.InvalidLoginException

    except m_e.InvalidLoginException:
        config_dict['user'] = User()

        return config_dict


def write_config(user):
    config = configparser.ConfigParser()
    config['user'] = user.login
    config['password'] = user.password


def write_user(login, password, new=False):
    config = configparser.ConfigParser()
    if not new:
        config.read(CONFIG_NAME)
    else:
        config['user'] = {'name': '', 'password': ''}

    config['user']['name'] = login
    config['user']['password'] = password

    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)


if not os.path.exists(CONFIG_NAME):
    write_user('', '', True)
