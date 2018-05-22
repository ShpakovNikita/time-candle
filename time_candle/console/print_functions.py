from enums.priority import priority_dict
from enums.status import status_dict


def print_tasks(tasks):
    for task in tasks:
        print_task(task)


def print_task(task):
    print('Task: {}, tid: {}, creator: {}, receiver: {}, deadline: {}, status: '
          '{}, priority: {}'.format(task.title, task.tid, task.creator_uid,
                                    task.uid, task.deadline,
                                    status_dict[task.status],
                                    priority_dict[task.priority]))


def print_users(users):
    for user in users:
        print_user(user)


def print_user(user):
    print('login: {}, nickname: {}, about: {}, mail: {}, id: {}'.
          format(user.login, user.nickname, user.about, user.mail, user.uid))


def print_projects(projects):
    for project in projects:
        print_project(project)


def print_project(project):
    print('id: {}, title: {}, admin id: {}, description: {}'.
          format(project.pid, project.title, project.admin_uid,
                 project.description))
