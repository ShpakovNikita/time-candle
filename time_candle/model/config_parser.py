import configparser
import time_candle.app_logger
import time_candle.exceptions.model_exceptions as m_e
import time_candle.storage.user_adapter
from time_candle.model.instances.user import User
import time_candle.exceptions.db_exceptions as db_e


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
                                             'login': 'Guest',
                                             'nickname': 'SansTheSkeleton',
                                             'about': '',
                                             'mail': None})
        try:
            config_dict['user'] = time_candle.storage.user_adapter.UserAdapter.\
                login_user(login, password)

        except db_e.InvalidPasswordError:
            config_dict['user'] = user_field()

        except db_e.InvalidLoginError:
            config_dict['user'] = user_field()
        return config_dict

    except KeyError:
        raise m_e.InvalidLoginException

    except m_e.InvalidLoginException:
        config_dict['user'] = User()

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
