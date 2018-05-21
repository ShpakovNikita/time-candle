import configparser
import app_logger
import exceptions.exceptions
import storage.user_adapter
from model.main_instances.user import User
import exceptions.db_exceptions as db_e

CONFIG_NAME = 'config.ini'
logger = app_logger.custom_logger('model')


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
        logger.debug('login has been set {} {}'.format(login, password))

        user_field = type('user_field', (), {'uid': None})
        try:
            config_dict['user'] = storage.user_adapter.UserAdapter.login_user(
                login, password)

        except db_e.InvalidPasswordError:
            logger.debug('Invalid password! Now you act like a guest here')
            config_dict['user'] = user_field()

        except db_e.InvalidLoginError:
            logger.debug('Invalid login! Now you act like a guest here')
            config_dict['user'] = user_field()
        return config_dict

    except KeyError:
        raise exceptions.exceptions.InvalidLoginException

    except exceptions.exceptions.InvalidLoginException:
        config_dict['user'] = User()
        logger.debug('user is invalid. Logging as guest')

        return config_dict


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
