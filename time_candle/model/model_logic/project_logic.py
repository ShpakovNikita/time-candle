from model.main_instances.project import Project as ProjectInstance
import exceptions.db_exceptions as db_e
from storage.project_adapter import ProjectFilter
from . import Logic


class ProjectLogic(Logic):

    def __init__(self, db_name=None):
        super().__init__(db_name)

    def add_user_to_project(self, login, pid):
        # add user to the project
        self.user_adapter.add_user_to_project_by_id(login, pid)

    def remove_user_from_project(self, login, pid):
        # remove user from project
        self.user_adapter.remove_from_project_by_login(login, pid)

    def add_project(self, title, description, members):
        # add project to the database
        project = ProjectInstance(self.project_adapter.last_id() + 1,
                                  self.user.uid,
                                  title,
                                  description)

        self.project_adapter.save(project)

        # if we cannot add one member from list, we delete project and it's
        # relations
        try:
            for login in members:
                self.add_user_to_project(login, project.pid)

        except db_e.InvalidLoginError:
            self.project_adapter.remove_project_by_id(project.pid)
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    def remove_project(self, pid):
        # remove project from database if have rights
        self.project_adapter.remove_project_by_id(pid)

    def change_project(self, pid, title, description):
        # change project in the database
        project = ProjectInstance.make_project(
            self.project_adapter.get_project_by_id(pid))
        if description is not None:
            project.description = description
        if title is not None:
            project.title = title

        self.project_adapter.save(project)

    def get_projects(self, substr):
        # get projects by passed substring
        fil = ProjectFilter().title_substring(substr)
        projects = self.project_adapter.get_by_filter(fil)
        return [ProjectInstance.make_project(project) for project in projects]
