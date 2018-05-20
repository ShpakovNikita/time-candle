from storage.adapter_classes import User, Task, Project, UserProjectRelation
from storage.adapter_classes import Filter as PrimaryFilter
from storage.adapter_classes import Adapter as PrimaryAdapter
import exceptions.db_exceptions as db_e
from peewee import *
from storage import logger


class UserFilter(PrimaryFilter):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _union_filter():
        return User.uid.is_null(False)

    def uid(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.uid == uid)
        return self

    def login_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(substring))
        return self

    def login_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(regex))
        return self

    def nickname_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(substring))
        return self

    def nickname_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(regex))
        return self


class UserAdapter(PrimaryAdapter):
    def __init__(self, db_name=None, uid=None):
        super().__init__(uid, db_name)

    @staticmethod
    def get_users_by_filter(filter_instance):
        """
        This function returns model objects by the given UserFilter.
        :param filter_instance: UserFilter with defined filters
        :return: List of UserInstances
        """
        query = User.select().where(filter_instance.to_query())

        result = [user for user in query]
        return result

    @staticmethod
    def login_user(login, password):
        """
        This function is like head function for all adapters. From this start
        point we get real user from database by it's login and valid password
        :param login: login of searching user
        :param password: password of searching user
        :type login: String
        :type password: String
        :return: User
        """
        query = User.select().where(User.login == login)

        try:
            # user instance
            obj = query.get()

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                str(db_e.LoginMessages.USER_DOES_NOT_EXISTS) +
                ', try to login again')

        if obj.password != password:
            raise db_e.InvalidPasswordError(
                db_e.PasswordMessages.PASSWORD_IS_NOT_MATCH)

        return obj

    @staticmethod
    def add_user(login, password, nickname=None):
        """
        This function if checking is current user exists, and if so we are
        raising an exception. Or we are adding it to the database.
        :param login: String
        :param password: String
        :param nickname: String
        :return: None
        """
        if User.select().where(User.login == login).exists():
            raise db_e.InvalidLoginError(db_e.LoginMessages.USER_EXISTS)

        if not nickname:
            nickname = login

        User.create(login=login,
                    password=password,
                    about='Hello, it\'s me, {}'.format(login),
                    nickname=nickname)

    def add_user_to_project_by_id(self, login, pid):
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
            project = Project.select(). \
                where((self.uid == Project.admin) &
                      (Project.pid == pid)).get()
            logger.debug('such project exists')

        except DoesNotExist:
            raise db_e.InvalidPidError(
                db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

        try:
            # we trying to find user by login
            user = User.select().where(User.login == login).get()
            logger.debug('such user exists')

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

        try:
            # and now we are checking if selected user already in the project.
            # If the exception DoesNotExist was not raised, that means that user
            # already in project and it's bad
            UserProjectRelation.select(). \
                where((UserProjectRelation.project == pid) &
                      (UserProjectRelation.user == user.uid)).get()

            logger.debug('such relation exists')
            raise db_e.InvalidLoginError(
                db_e.ProjectMessages.USER_ALREADY_EXISTS)
        except DoesNotExist:
            logger.debug('such user is not in project')

            UserProjectRelation.create(user=user, project=project)

        logger.info('user_project relation created')

    def remove_from_project_by_login(self, login, pid):
        """
        This function removes user from the project by it's login
        :param pid: Project's id
        :param login: User's login
        :return: None
        """
        uid = UserAdapter.get_id_by_login(login)

        try:
            # we get task where current user is admin and where project id is
            # matching
            Project.select().where(
                (self.uid == Project.admin) & (Project.pid == pid)).get()
            logger.debug('such project exists')
            # if an admin tries to delete himself we deny it
            if uid == self.uid:
                raise db_e.InvalidPidError(
                    db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

        except DoesNotExist:
            # not admin can try to delete himself
            if uid != self.uid:
                raise db_e.InvalidPidError(
                    db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

        # now we try to find and delete user
        rows = UserProjectRelation.delete().where(
            (UserProjectRelation.project == pid) &
            (UserProjectRelation.user == uid)).\
            execute()

        if rows == 0:
            raise db_e.InvalidLoginError(db_e.LoginMessages.NO_USER_TO_DELETE)

    @staticmethod
    def get_id_by_login(login):
        """
        This function checks if user by passed login exists in the database and
        returns user's id, or raises an error
        :param login: User's login
        :return: Int
        """
        try:
            return User.select(). \
                where(User.login == login).get().uid

        except DoesNotExist:
            db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    @staticmethod
    def get_user_by_id(uid):
        """
        This function returns login of user by id
        :param uid: User's id
        :return: String
        """
        query = User.select().where(User.uid == uid)
        try:
            # user instance
            obj = query.get()

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

        return obj

    # TODO: maybe add function get_id_by_login to change all login on uid
    @staticmethod
    def is_user_in_project(login, pid):
        """
        This function checks if passed user exists in the selected project
        :param login: User's login
        :param pid: Project's id
        :return: Bool
        """
        uid = UserAdapter.get_id_by_login(login)
        logger.debug('the uid is %s' % uid)

        try:
            UserProjectRelation.select(). \
                where((UserProjectRelation.project == pid) &
                      (UserProjectRelation.user == uid)).get()

            logger.debug('user exists in project')
            return True

        except DoesNotExist:
            raise db_e.InvalidPidError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)
