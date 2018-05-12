from main_instances.user import User as UserInstance
from storage.adapter_classes import User, Task, Project, UserProjectRelation
from storage.adapter_classes import Filter as PrimaryFilter
import exceptions.db_exceptions as db_e
from peewee import *
from singleton import Singleton
from storage import logger


class UserFilter(PrimaryFilter):

    def __init__(self):
        super().__init__()

    def uid(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.id == uid)

    def login_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(substring))

    def login_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(regex))

    def nickname_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(substring))

    def nickname_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(regex))


def get_users_by_filter(filter_instance):
    """
    This function returns model objects by the given UserFilter.
    :param filter_instance: UserFilter with defined filters
    :return: List of UserInstances
    """
    result = []
    query = User.select().where(filter_instance.to_query())

    for user in query:
        result.append(_storage_to_model(user))

    return result


def login_user(login, password):
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
        raise db_e.InvalidLoginError(
            str(db_e.LoginMessages.USER_DOES_NOT_EXISTS) +
            ', try to login again')

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


def add_user(login, password):
    """
    This function if checking is current user exists, and if so we are raising
    an exception. Or we are adding it to the database.
    :param login: String
    :param password: String
    :return: None
    """
    if User.select().where(User.login == login).exists():
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_EXISTS)

    user = User.create(login=login,
                       password=password,
                       about='Hello, it\'s me, {}'.format(login))

    # Maybe it is better to fix it in another way. Here we are defining nickname
    # same as the login
    if not user.nickname:
        user.nickname = user.login
        user.save()


def add_user_to_project_by_id(login, pid):
    """
    This function adds user to the Project relationship table to make user a 
    member of the project, if both exists.
    :param login: User's login
    :param pid: Project's id
    :return: None
    """
    try:
        # we get task where current user is admin and where project id is
        # matching
        project = Project.select().\
            where((Singleton.GLOBAL_USER.uid == Project.admin) &
                  (Project.id == pid)).get()
        logger.debug('such project exists')

    except DoesNotExist:
        raise db_e.InvalidPidError(db_e.ProjectMessages.YOU_DO_NOT_HAVE_RIGHTS)

    try:
        # we trying to find user by login
        user = User.select().where(User.login == login).get()
        logger.debug('such user exists')

    except DoesNotExist:
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    try:
        # and now we are checking if selected user already in the project. If
        # the exception DoesNotExist was not raised, that means that user
        # already in project and it's bad
        UserProjectRelation.select().\
            where((UserProjectRelation.project == pid) &
                  (UserProjectRelation.user == user.id)).get()

        logger.debug('such relation exists')
        raise db_e.InvalidLoginError(db_e.ProjectMessages.USER_ALREADY_EXISTS)
    except DoesNotExist:
        logger.debug('such user is not in project')

        UserProjectRelation.create(user=user, project=project)

    logger.info('user_project relation created')


def get_id_by_login(login):
    """
    This function checks if user by passed login exists in the database and
    returns user's id, or raises an error
    :param login: User's login
    :return: Int
    """
    try:
        return User.select().\
               where(User.login == login).get().id

    except DoesNotExist:
        db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)


def get_user_by_id(uid):
    """
    This function returns login of user by id
    :param uid: User's id
    :return: String
    """
    query = User.select().where(User.id == uid)
    try:
        obj = query.get()

    except DoesNotExist:
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    return UserInstance(obj.id,
                        obj.login,
                        obj.password,
                        obj.time_zone,
                        obj.nickname,
                        obj.about)


# TODO: maybe add function get_id_by_login to change all login on uid
def is_user_in_project(login, pid):
    """
    This function checks if passed user exists in the selected project
    :param login: User's login
    :param pid: Project's id
    :return: Bool
    """
    uid = get_id_by_login(login)
    logger.debug('the uid is %s' % uid)

    try:
        UserProjectRelation.select().\
            where((UserProjectRelation.project == pid) &
                  (UserProjectRelation.user == uid)).get()

        logger.debug('user exists in project')
        return True

    except DoesNotExist:
        raise db_e.InvalidPidError(db_e.LoginMessages.USER_DOES_NOT_EXISTS )


def get_tasks_id_by_uid(uid):
    """
    This function returns task id's of each personal user's task
    :param: User's id
    :return: List of tids
    """
    query = Task.select(Task.id).where((Task.creator == uid) &
                                       (Task.receiver == uid) &
                                       Task.project.is_null(True))

    return [tid.id for tid in query]


def get_projects_id_by_uid(uid):
    """
    This function returns projects id's of each project where user is named
    :param: User's id
    :return: List of pids
    """
    query = Task.select(UserProjectRelation.project).\
        where(UserProjectRelation.user == uid)

    return [pid.id for pid in query]


def _storage_to_model(storage_user):
    """
    This function converts storage user to model user
    :type storage_user: User
    :return: UserInstance
    """
    logger.debug('convert storage to model user')

    model_user = UserInstance(storage_user.id,
                              storage_user.login,
                              storage_user.password,
                              storage_user.time_zone,
                              storage_user.nickname,
                              storage_user.about)

    return model_user
