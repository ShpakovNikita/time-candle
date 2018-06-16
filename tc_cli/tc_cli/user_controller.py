from tc_cli.user import User as UserInstance
from tc_cli.user_adapter import UserAdapter
from tc_cli.config_parser import run_config
import time_candle.exceptions.db_exceptions as db_e
from tc_cli import user_validation as v
from tc_cli import config_parser
from tc_cli import logger
from copy import copy


class UserAuthenticationController:

    def __init__(self, db_file=None, uid=None):
        self.user_adapter = UserAdapter(db_file)
        self._auth(uid)

    def _auth(self, uid=None):
        """
        Returns loaded user to make some actions from it's name. User will be
        initialized from config file.
        :param uid: User's id.
        :return: None
        """
        if uid is not None:
            self.uid = uid
        else:
            self.uid = self.load_user().uid

        self.user_adapter.uid = self.uid

    @staticmethod
    def load_user():
        return run_config()['user']

    def add_user(self, login, password, mail=None):
        """
        This function adds user to auth database
        :param mail: User's email
        :param login: User's login
        :param password: User's password
        :return: None
        """
        v.check_login(login)
        v.check_password(password)
        user = UserInstance(login=login, password=password)
        self.user_adapter.save(user)
        return self.user_adapter.get_id_by_login(login)

    def log_in(self, login, password):
        """
        This function writes current user to the config.ini
        :type login: String
        :type password: String
        :return: Bool
        """
        # logging in writing the config file
        success = False
        try:
            UserInstance.make_user(
                self.user_adapter.authenticate(login, password))

            success = True
        except db_e.InvalidPasswordError:
            logger.info('Invalid password! Now you act like a guest here')

        except db_e.InvalidLoginError:
            logger.info('Invalid login! Now you act like a guest here')

        # if everything is ok, we will write our login and password to the
        # config.ini
        config_parser.write_user(login, password)
        return success

    def authenticate(self):
        """
        This function authenticates current user
        :return: None
        """
        user = self.load_user()
        self.user_adapter.authenticate(user.login, user.password)
        logger.info('Successfully authenticated!')

    def get_current_user(self):
        """
        This function returns current user.
        :return: UserInstance
        """
        user = self.load_user()
        return copy(user)

    @staticmethod
    def logout():
        """
        This function logging out current user.
        :return: None
        """
        # logging out writing the blank lines to the config
        config_parser.write_user('', '')
