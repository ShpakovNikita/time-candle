from model.model_logic import *


def add_user_to_project(login, pid):
    # add user to the project
    Adapters.USER_ADAPTER.add_user_to_project_by_id(login, pid)


def add_project(title, description, members):
    # add project to the database
    project = ProjectInstance(Adapters.PROJECT_ADAPTER.last_id() + 1,
                              Singleton.GLOBAL_USER.uid,
                              title,
                              description)

    Adapters.PROJECT_ADAPTER.save(project)

    # if we cannot add one member from list, we delete project and it's
    # relations
    try:
        for login in members:
            add_user_to_project(login, project.pid)

    except db_e.InvalidLoginError:
        Adapters.PROJECT_ADAPTER.remove_project_by_id(project.pid)
        raise db_e.InvalidLoginError(db_e.LoginMessages.USER_DOES_NOT_EXISTS)
