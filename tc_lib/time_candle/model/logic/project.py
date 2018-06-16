from time_candle.model.instances.project import Project as ProjectInstance
import time_candle.exceptions.db_exceptions as db_e
from time_candle.storage.project_adapter import ProjectFilter
from time_candle.model.logic import Logic
from time_candle.model.instances.user import User


class ProjectLogic(Logic):

    def __init__(self, db_name=None, uid=None, psql_config=None):
        super().__init__(db_name, uid, psql_config)

    def add_user_to_project(self, uid, pid):
        # add user to the project
        self.project_adapter.add_user_to_project_by_id(uid, pid)

    def remove_user_from_project(self, uid, pid):
        # remove user from project
        self.project_adapter.remove_from_project_by_id(uid, pid)

    def add_project(self, title, description, members):
        # add project to the database
        project = ProjectInstance(self.project_adapter.last_id() + 1,
                                  self.uid,
                                  title,
                                  description)

        self.project_adapter.save(project)

        # if we cannot add one member from list, we delete project and it's
        # relations
        try:
            for uid_p in members:
                self.add_user_to_project(uid_p, project.pid)

        except db_e.InvalidLoginError:
            self.project_adapter.remove_project_by_id(project.pid)
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    def remove_project(self, pid):
        # remove project from database if have rights
        self.project_adapter.remove_project_by_id(pid)

    def get_project(self, pid):
        fil = ProjectFilter().pid(pid)
        try:
            return self.project_adapter.get_by_filter(fil)[0]
        except IndexError:
            raise db_e.InvalidPidError(
                db_e.ProjectMessages.PROJECT_DOES_NOT_EXISTS)

    def change_project(self, pid, title, description):
        # change project in the database
        project = self.project_adapter.get_project_by_id(pid)
        if description is not None:
            project.description = description
        if title is not None:
            project.title = title

        self.project_adapter.save(project)

    def get_projects(self, substr):
        # get projects by passed substring
        fil = ProjectFilter().title_substring(substr)
        projects = self.project_adapter.get_by_filter(fil)
        return projects

    def get_users(self, pid):
        # get users
        users = self.project_adapter.get_users_by_project(pid)
        return users
