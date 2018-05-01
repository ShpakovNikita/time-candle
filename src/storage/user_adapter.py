import storage.adapter_classes
from main_instances.user import User as UserInstance
from storage.adapter_classes import User, Task
import exceptions.db_exceptions as db_e


def get_user(login, password):
    """
    This function is like head function for all adapters. From this start point
    we get real user from database by it's login and valid password
    :param login: login of searching user
    :param password: password of searching user
    :type login: String
    :type password: String
    :return: User
    """
    query = User.select().where(User.login == login)
    obj = query.get()
    if not query.exists():
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_NOT_EXISTS)

    elif obj.password != password:
        raise db_e.InvalidPasswordError(db_e.PasswordMessages.
                                        PASSWORD_IS_NOT_MATCH)

    return UserInstance(obj.id,
                        obj.login,
                        obj.password,
                        obj.time_zone,
                        obj.nickname,
                        obj.about)
