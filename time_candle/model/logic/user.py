from time_candle.model.instances.user import User as UserInstance
import time_candle.exceptions.db_exceptions as db_e
from time_candle.model import config_parser
from time_candle.model import logger
from time_candle.storage.user_adapter import UserFilter
from . import Logic


class UserLogic(Logic):

    def __init__(self, db_name=None):
        super().__init__(db_name)

    def log_in(self, login, password):
        # logging in writing the config file
        success = False
        try:
            UserInstance.make_user(
                self.user_adapter.login_user(login, password))

            success = True
        except db_e.InvalidPasswordError:
            logger.info('Invalid password! Now you act like a guest here')

        except db_e.InvalidLoginError:
            logger.info('Invalid login! Now you act like a guest here')

        # if everything is ok, we will write our login and password to the
        # config.ini
        config_parser.write_user(login, password)
        return success

    def add_user(self, login, password, nickname, about, mail):
        # add user to the database
        user = UserInstance(login=login,
                            password=password,
                            nickname=nickname,
                            about=about,
                            mail=mail)
        self.user_adapter.save(user)

    def get_users(self, substr, pid=None):
        # get users by passed substring
        fil = UserFilter().nickname_substring(substr)
        if pid is not None:
            users = self.user_adapter.get_by_project(pid)
        else:
            users = self.user_adapter.get_by_filter(fil)

        return [UserInstance.make_user(user) for user in users]

    @staticmethod
    def logout():
        # logging out writing the blank lines to the config
        config_parser.write_user('', '')
