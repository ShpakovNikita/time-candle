from model.main_instances.user import User as UserInstance
from storage import *
import exceptions.db_exceptions as db_e
from model import config_parser
from model.session_control import Singleton, Adapters
from model import logger
from storage.user_adapter import UserFilter


def log_in(login, password):
    # logging in writing the config file
    success = False
    try:
        UserInstance.make_user(
            Adapters.USER_ADAPTER.login_user(login, password))

        success = True
    except db_e.InvalidPasswordError:
        logger.info('Invalid password! Now you act like a guest here')

    except db_e.InvalidLoginError:
        logger.info('Invalid login! Now you act like a guest here')

    # if everything is ok, we will write our login and password to the
    # config.ini
    config_parser.write_user(login, password)
    return success


def add_user(login, password, nickname, about, mail):
    # add user to the database
    user = UserInstance(login=login,
                        password=password,
                        nickname=nickname,
                        about=about,
                        mail=mail)
    Adapters.USER_ADAPTER.save(user)


def get_users(substr, pid=None):
    # get users by passed substring
    fil = UserFilter().nickname_substring(substr)
    if pid is not None:
        users = Adapters.USER_ADAPTER.get_by_project(pid)
    else:
        users = Adapters.USER_ADAPTER.get_by_filter(fil)

    return [UserInstance.make_user(user) for user in users]


def logout():
    # logging out writing the blank lines to the config
    config_parser.write_user('', '')
