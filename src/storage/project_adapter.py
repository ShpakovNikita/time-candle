from peewee import *
from storage.adapter_classes import Project, UserProjectRelation
from storage.adapter_classes import Filter as PrimaryFilter
from storage.adapter_classes import Adapter as PrimaryAdapter
import exceptions.db_exceptions as db_e
from storage import logger


class ProjectFilter(PrimaryFilter):

    def __init__(self):
        super().__init__()

    def pid(self, pid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.admin == pid)

    def admin(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.admin == uid)

    def title(self, title, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.title == title)

    def description_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.description.contains(substring))

    def description_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Project.description.regexp(regex))


class ProjectAdapter(PrimaryAdapter):
    def __init__(self, db_name=None, uid=None):
        super().__init__(uid, db_name)

    def save(self, obj):
        """
        This function is used to store given project in database
        :param obj: type with fields:
        - admin_uid
        - description
        - title
        :return: None
        """

        try:
            project = Project(admin=obj.admin_uid,
                              description=obj.description,
                              title=obj.title)

            relation = UserProjectRelation(user=self.uid,
                                           project=project)

            print(self.uid, obj.admin_uid, relation.project)
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
        # TODO: FIX (need relations)
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
            raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)

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
                                   (Project.admin == self.uid))

            return True

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)

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

            Project.delete(). \
                where(Project.pid == pid).execute()

            logger.debug('project fully removed')

        except DoesNotExist:
            db_e.InvalidPidError(db_e.ProjectMessages.PROJECT_DOES_NOT_EXISTS)

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
            return 1
