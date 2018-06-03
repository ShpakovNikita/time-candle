from peewee import DoesNotExist, IntegrityError
from time_candle.storage.adapter_classes import Project, UserProjectRelation, Task
from time_candle.storage.adapter_classes import Filter as PrimaryFilter
from time_candle.storage.adapter_classes import Adapter as PrimaryAdapter
import time_candle.exceptions.db_exceptions as db_e
from time_candle.storage import logger


class ProjectFilter(PrimaryFilter):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _union_filter():
        return Project.pid.is_null(False)

    def pid(self, pid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.admin == pid)
        return self

    def admin(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.admin == uid)
        return self

    def title_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.title.contains(substring))
        return self

    def title_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.title.regexp(regex))
        return self

    def description_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.description.contains(substring))
        return self

    def description_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.description.regexp(regex))
        return self


class ProjectAdapter(PrimaryAdapter):
    def __init__(self, db_name=None, uid=None):
        super().__init__(uid, db_name)

    def get_by_filter(self, filter_instance):
        """
        This function returns storage objects by the given ProjectFilter.
        :param filter_instance: ProjectFilter with defined filters
        :return: List of Project objects
        """
        # in this query we get all available projects
        query = self._get_available_projects().select().\
            where(filter_instance.to_query())

        # return converted query to the outer module
        result = [project for project in query]
        return result

    def save(self, obj):
        """
        This function is used to store given project in database
        :param obj: type with fields:
        - pid
        - admin_uid
        - description
        - title
        :return: None
        """
        try:
            self.has_rights(obj.pid)
            project = Project.select().where(Project.pid == obj.pid).get()
            self._update(project, obj)
            return
        except db_e.InvalidPidError:
            logger.debug('adding project...')

        try:
            project = Project(admin=obj.admin_uid,
                              description=obj.description,
                              title=obj.title)

            relation = UserProjectRelation(user=self.uid,
                                           project=project)

            # only if everything is ok we try save project to our database
            project.save()
            relation.save()

        except IntegrityError:
            # if you are guest
            raise db_e.InvalidLoginError(
                db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

        logger.debug('project saved to database')

    def get_project_by_id(self, pid):
        """
        This function finds project by id and current user in database and
        returns it or raise error due to incorrect request
        :param pid: Project id to find
        :type pid: Int
        :return: Project
        """
        try:
            # we are checking if there is a connection our user and selected
            # project
            UserProjectRelation.select(). \
                where((UserProjectRelation.user == self.uid) &
                      (UserProjectRelation.project == pid)).get()

            # if so, ge get this project by pid
            project = Project.select().where((Project.pid == pid))

            return project.get()

        except DoesNotExist:
            logger.info('There is no such pid %s in the database for your user'
                        % pid)
            raise db_e.InvalidPidError(
                db_e.ProjectMessages.PROJECT_DOES_NOT_EXISTS)

    def has_rights(self, pid):
        """
        This function checks if logged user has rights to do something inside
        the project
        :param pid: Project's id
        :return: Bool
        """
        try:
            Project.select().where(Project.pid == pid).get()

        except DoesNotExist:
            raise db_e.InvalidPidError(
                db_e.ProjectMessages.PROJECT_DOES_NOT_EXISTS)

        try:
            Project.select().where((Project.pid == pid) &
                                   (Project.admin == self.uid)).get()

            return True

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

    def add_user_to_project_by_id(self, uid, pid):
        """
        This function adds user to the Project relationship table to make user a
        member of the project, if both exists.
        :param uid: User's id
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

        # NOTE: due to we don't have access to the users db, we BELIEVE, that
        # user exists in the database (you should check that on the auth level)

        try:
            # and now we are checking if selected user already in the project.
            # If the exception DoesNotExist was not raised, that means that user
            # already in project and it's bad
            UserProjectRelation.select(). \
                where((UserProjectRelation.project == pid) &
                      (UserProjectRelation.user == uid)).get()

            logger.debug('such relation exists')
            raise db_e.InvalidLoginError(
                db_e.ProjectMessages.USER_ALREADY_EXISTS)
        except DoesNotExist:
            logger.debug('such user is not in project')

            UserProjectRelation.create(user=uid, project=project)

        logger.info('user_project relation created')

    def remove_from_project_by_id(self, uid, pid):
        """
        This function removes user from the project by it's id
        :param pid: Project's id
        :param uid: User's id
        :return: None
        """
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
            raise db_e.InvalidUidError(db_e.LoginMessages.NO_USER_TO_DELETE)

    # TODO: maybe add function get_id_by_login to change all login on uid
    @staticmethod
    def is_user_in_project(uid, pid):
        """
        This function checks if passed user exists in the selected project
        :param uid: User's id
        :param pid: Project's id
        :return: Bool
        """
        logger.debug('the uid is %s' % uid)

        try:
            UserProjectRelation.select(). \
                where((UserProjectRelation.project == pid) &
                      (UserProjectRelation.user == uid)).get()

            logger.debug('user exists in project')
            return True

        except DoesNotExist:
            raise db_e.InvalidPidError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    def get_users_by_project(self, pid):
        self.is_user_in_project(self.uid, pid)

        query = UserProjectRelation.select().\
            where(UserProjectRelation.project == pid)

        return [q.user for q in query]

    def remove_project_by_id(self, pid):
        """
        This function removes project from id snd clears all relations between
        users and passed project. Or it raises an exception if you don't have
        rights or pid do not exists
        :param pid: Project's id
        :return: None
        """
        self.has_rights(pid)

        try:
            UserProjectRelation.delete(). \
                where(UserProjectRelation.project == pid).execute()

            Project.delete().where(Project.pid == pid).execute()

            Task.delete().where(Task.project == pid).execute()

            logger.debug('project fully removed')

        except DoesNotExist:
            db_e.InvalidPidError(db_e.ProjectMessages.PROJECT_DOES_NOT_EXISTS)

    @staticmethod
    def _update(project, obj):
        project.admin = obj.admin_uid
        project.description = obj.description
        project.title = obj.title

        project.save()

    @staticmethod
    def last_id():
        """
        This function gets last id to add project on it's place
        TODO:
        This function finds the first unused id in the table to add new project
        row on that place
        :return: Int
        """

        query = Project.select().order_by(Project.pid.desc())
        logger.debug('getting last id from query...{}'.format(query))

        try:
            # project query
            return query.get().pid

        except DoesNotExist:
            return 0

    def _get_available_projects(self):
        # get all tasks in project related to user
        query_projects = Project.select(). \
            join(UserProjectRelation).\
            where(UserProjectRelation.user == self.uid)

        return query_projects
