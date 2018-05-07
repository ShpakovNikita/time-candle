import app_logger
from peewee import *
from storage.adapter_classes import Project, UserProjectRelation
from singleton import Singleton
from main_instances.project import Project as ProjectInstance
import exceptions.db_exceptions as db_e


def save(project_model):
    """
    This function is used to store given project in database
    :param project_model: This is our task to save
    :type project_model: ProjectInstance
    :return: None
    """

    project = Project(admin=project_model.admin_uid,
                      description=project_model.description,
                      title=project_model.title)

    relation = UserProjectRelation(user=Singleton.GLOBAL_USER.uid,
                                   project=project)

    # only if everything is ok we save project to our database
    project.save()
    relation.save()

    app_logger.custom_logger('storage').debug('project saved to database')


def last_id():
    """
    This function gets last id to add project on it's place
    TODO:
    This function finds the first unused id in the table to add new project row
    on that place
    :return: Int
    """

    query = Project.select().order_by(Project.id.desc())
    app_logger.custom_logger('storage').debug('getting last id from query...{}'
                                              .format(query))

    try:
        return query.get().id

    except DoesNotExist:
        return 1


def get_project_by_id(pid):
    """
    This function finds project by id and current user in database and returns
    it or raise error due to incorrect request
    :param pid: Project id to find
    :type pid: Int
    :return: Project
    """
    # TODO: FIX (need relations)
    try:
        # we are checking if there is a connection our user and selected project
        UserProjectRelation.select().\
            where((UserProjectRelation.user == Singleton.GLOBAL_USER.uid) &
                  (UserProjectRelation.project == pid)).get()

        # if so, ge get this project by pid
        project = Project.select().where((Project.id == pid))

        return _storage_to_model(project.get())

    except DoesNotExist:
        app_logger.custom_logger('storage').info('There is no such pid %s in '
                                                 'the database for your user' %
                                                 pid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def has_rights(pid):
    """
    This function checks if logged user has rights to do something inside the
    project
    :param pid: Project's id
    :return: Bool
    """
    try:
        Project.select().where((Project.id == pid) &
                               (Project.admin == Singleton.GLOBAL_USER.uid))

        return True

    except DoesNotExist:
        raise db_e.InvalidLoginError(db_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)


def _storage_to_model(storage_project):
    """
    This function converts storage project to model project
    :type storage_project: Project
    :return: ProjectInstance
    """
    app_logger.custom_logger('storage').\
        debug('convert storage to model project')

    model_project = ProjectInstance(storage_project.id,
                                    storage_project.admin.id)

    return model_project
