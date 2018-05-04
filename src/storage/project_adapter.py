import app_logger
from peewee import *
from storage.adapter_classes import Project
from singleton import Singleton
from main_instances.project import Project as ProjectInstance


def save(project):
    """
    This function is used to store given project in database
    :param project: This is our task to save
    :type project: ProjectInstance
    :return: None
    """

    Project.create(admin=project.admin_uid)
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
