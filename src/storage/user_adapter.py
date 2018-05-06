from main_instances.user import User as UserInstance
from storage.adapter_classes import User, Task, Project, UserProjectRelation
import exceptions.db_exceptions as db_e
from peewee import *
from singleton import Singleton
import app_logger


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
    try:
        obj = query.get()

    except DoesNotExist:
        raise db_e.InvalidLoginError(str(db_e.LoginMessages.USER_DOES_NOT_EXISTS
                                         ) + ', try to login again')

    if not query.exists():
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    elif obj.password != password:
        raise db_e.InvalidPasswordError(db_e.PasswordMessages.
                                        PASSWORD_DOES_IS_NOT_MATCH)

    return UserInstance(obj.id,
                        obj.login,
                        obj.password,
                        obj.time_zone,
                        obj.nickname,
                        obj.about)


def add_user_to_project_by_id(login, pid):
    """
    This function adds user to the Project relationship table to make user a 
    member of the project, if both exists.
    :param login: User's login
    :param pid: Project's id
    :return: None
    """
    print('123')
    try:
        # we get task where current user is admin and where project id is
        # matching
        project = Project.select().\
            where((Singleton.GLOBAL_USER.uid == Project.admin) &
                  (Project.id == pid)).get()
        app_logger.custom_logger('storage').debug('such project exists')

    except DoesNotExist:
        raise db_e.InvalidPidError(db_e.ProjectMessages.YOU_DO_NOT_HAVE_RIGHTS)

    try:
        # we trying to find user by login
        user = User.select().where(User.login == login).get()
        app_logger.custom_logger('storage').debug('such user exists')

    except DoesNotExist:
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    try:
        # and now we are checking if selected user already in the project. If
        # the exception DOesNotExist was not raised, that means that user
        # already in project and it's bad
        UserProjectRelation.select().\
            where((UserProjectRelation.project == pid) &
                  (UserProjectRelation.user == user.id)).get()

        raise db_e.InvalidLoginError(db_e.ProjectMessages.USER_ALREADY_EXISTS)
    except DoesNotExist:
        app_logger.custom_logger('storage').debug('such user is not in project')

        UserProjectRelation.create(user=user, project=project)

    app_logger.custom_logger('storage').info('user_project relation created')

