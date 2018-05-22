from model.model_logic import *


def log_in(login, password):
    # logging in writing the config file
    try:
        UserInstance.make_user(
            Adapters.USER_ADAPTER.login_user(login, password))
    except db_e.InvalidPasswordError:
        logger.debug('Invalid password! Now you act like a guest here')

    except db_e.InvalidLoginError:
        logger.debug('Invalid login! Now you act like a guest here')

    # if everything is ok, we will write our login and password to the
    # config.ini
    config_parser.write_user(login, password)


def add_user(login, password, nickname, about, mail):
    # add user to the database
    user = UserInstance(login=login,
                        password=password,
                        nickname=nickname,
                        about=about,
                        mail=mail)
    Adapters.USER_ADAPTER.save(user)


def get_users(substr):
    # get users by passed substring
    fil = UserFilter().nickname_substring(substr)
    users = Adapters.USER_ADAPTER.get_by_filter(fil)
    return [UserInstance.make_user(user) for user in users]


def logout():
    # logging out writing the blank lines to the config
    config_parser.write_user('', '')
