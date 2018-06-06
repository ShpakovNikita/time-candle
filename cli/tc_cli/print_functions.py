from time_candle.enums.priority import priority_dict
from time_candle.enums.status import status_dict
import time_candle.model.time_formatter
import os


def print_tasks(tasks):
    for task in tasks:
        print_task(task)


def print_task(task):
    if task.deadline is not None:
        deadline_time = time_candle.model.time_formatter.\
            get_datetime(task.deadline)
    else:
        deadline_time = 'unlimited'

    if task.realization_time is not None:
        realization_time = time_candle.model.\
            time_formatter.get_datetime(task.realization_time)
    else:
        realization_time = 'undone'

    # TODO: CURSES
    print('==============@_@==============')
    print('task: {}, \t creator: {}, \t receiver: {}, \t period: {} \n'
          'deadline: {}, \t status: {}, \t realization time: {}, \n'
          'creation time: {}, \t priority: {}, \t project id: {}, \t tid: {}'.
          format(task.title, task.creator_uid, task.uid, task.period,
                 deadline_time, status_dict[task.status], realization_time,
                 time_candle.model.time_formatter.
                 milliseconds_to_string(task.creation_time)
                 , priority_dict[task.priority], task.pid, task.tid))


def print_users(users):
    for user in users:
        print_user(user)


def print_user(user):
    info = ('login: {}, nickname: {}, about: {}, mail: {}, id: {}'.
            format(user.login, user.nickname, user.about, user.mail, user.uid))
    print(info)


def cow_print_user(user):
    info = ('login: {}, nickname: {}, about: {}, mail: {}, id: {}'.
            format(user.login, user.nickname, user.about, user.mail, user.uid))

    os.system('cowsay ' + '"' + info + '"')


def print_projects(projects):
    for project in projects:
        print_project(project)


def print_project(project):
    print('id: {}, title: {}, admin id: {}, description: {}'.
          format(project.pid, project.title, project.admin_uid,
                 project.description))


def watch():
    os.system('telnet towel.blinkenlights.nl')
