import configparser
import app_logger
import exceptions.exceptions
import storage.user_adapter

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
        login = config['user']['name']
        password = config['user']['password']

        # Create user by it's name and password. If it exists, we will get it
        # from database
        app_logger.custom_logger('model').debug('login has been set {} {}'.
                                                format(login, password))
        config_dict['user'] = storage.user_adapter.get_user(login, password)
        return config_dict

    except KeyError:
        raise exceptions.exceptions.InvalidLoginException


def write_config(user):
    # TODO: Check if user is in database and password is correct
    config = configparser.ConfigParser()
    config['user'] = user.login
    config['password'] = user.password


def write_user(login, password):
    config = configparser.ConfigParser()
    config.read(CONFIG_NAME)

    config['user']['name'] = login
    config['user']['password'] = password

    with open(CONFIG_NAME, 'w') as configfile:
        config.write(configfile)
