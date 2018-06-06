from time_candle.module_app.user import User as UserInstance
from time_candle.module_app.user_adapter import UserAdapter, UserFilter
from time_candle.module_app.config_parser import run_config
import time_candle.module_app.user_validation as v
import time_candle.exceptions.db_exceptions as db_e
from time_candle.module_app import config_parser
from time_candle.module_app import logger
from copy import copy


class UserController:

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
            self.uid = self.auth().uid

        self.user_adapter.uid = self.uid

    @staticmethod
    def auth():
        return run_config()['user']

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

    def add_user(self,
                 login,
                 password,
                 mail=None,
                 nickname=None,
                 about=''):
        """
        This function adds user to the database, if there is no users with given
        login
        :type login: String
        :type password: String
        :type mail: String
        :type nickname: String
        :type about: String
        :return: None
        """
        if mail is not None:
            v.check_mail(mail)

        if nickname is None:
            nickname = login

        if not about:
            about = 'Hello, it\'s me, ' + nickname

        v.check_login(login)
        v.check_name(nickname)
        v.check_password(password)

        # add user to the database
        user = UserInstance(login=login,
                            password=password,
                            nickname=nickname,
                            about=about,
                            mail=mail)
        self.user_adapter.save(user)

    def get_users(self, substr):
        """
        This function returns found users.
        :param substr: Filter for nickname search
        :type substr: String
        :return: list of UserInstance
        """
        # get users by passed substring
        fil = UserFilter().nickname_substring(substr)
        users = self.user_adapter.get_by_filter(fil)

        return [UserInstance.make_user(user) for user in users]

    def get_current_user(self):
        """
        This function returns current user.
        :return: UserInstance
        """
        user = self.auth()
        return copy(user)

    @staticmethod
    def logout():
        """
        This function logging out current user.
        :return: None
        """
        # logging out writing the blank lines to the config
        config_parser.write_user('', '')
