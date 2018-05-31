import unittest
from storage.adapter_classes import Task, User, Project, UserProjectRelation
from storage.adapter_classes import Filter as PrimaryFilter
from storage.project_adapter import ProjectAdapter, ProjectFilter
from storage.user_adapter import UserAdapter, UserFilter
from storage.task_adapter import TaskAdapter, TaskFilter
from enums.priority import Priority
from enums.status import Status
import exceptions.db_exceptions as db_e
from copy import copy


db_file = ':memory:'


__all__ = ['_init_user_table', '_init_project_table',
           '_init_task_table', '_init_project_tasks_table', '_USERS',
           '_TASKS', '_PROJECTS', '_PROJECT_TASKS', 'db_file',
           'Task', 'User', 'Project', 'UserProjectRelation',
           'ProjectAdapter', 'ProjectFilter', 'unittest',
           'UserAdapter', 'UserFilter', 'TaskAdapter', 'TaskFilter',
           'Priority', 'Status', 'db_e', 'copy', 'PrimaryFilter',
           'UserDummie', 'ProjectDummie', 'TaskDummie']


def _project_init(self,
                  pid,
                  admin_uid,
                  title,
                  description=''):
    self.pid = pid
    self.admin_uid = admin_uid
    self.title = title
    self.description = description


ProjectDummie = type('ProjectDummie', (), {'__init__': _project_init})


# Task dummie
def _task_init(self,
               uid,
               creator_uid,
               tid,
               deadline,
               title,
               pid=None,
               status=Status.IN_PROGRESS,
               priority=Priority.MEDIUM,
               parent=None,
               comment='',
               realization_time=-1,
               creation_time=0,
               period=None):
    self.uid = uid
    self.creator_uid = creator_uid
    self.tid = tid
    self.pid = pid
    self.title = title
    self.status = status
    self.priority = priority
    self.parent = parent
    self.deadline = deadline
    self.comment = comment
    self.realization_time = realization_time
    self.creation_time = creation_time
    self.period = period


TaskDummie = type('TaskDummie', (), {'__init__': _task_init})


# User dummie.
def _user_init(self,
               uid=None,
               login='guest',
               password=None,
               time_zone=None,
               nickname='guest',
               about='',
               mail=None):
    self.uid = uid
    self.login = login
    self.nickname = nickname
    self.password = password
    self.time_zone = time_zone
    self.about = about
    self.mail = mail


UserDummie = type('UserDummie', (), {'__init__': _user_init})

_USERS = [
    UserDummie(uid=1, login='sanya', password='12345', nickname='SaNo228'),
    UserDummie(uid=2, login='Shaft', password='123', nickname='SaNo228'),
    UserDummie(uid=3, login='Arracias', password='12345', nickname='Boudart'),
    UserDummie(uid=4, login='Andy', password='123452', nickname='weratt'),
    UserDummie(uid=5, login='sanga', password='Yanix', nickname='BPATUIIIKA'),
    UserDummie(uid=6, login='Sashya', password='Ya', nickname='SanEk'),
    UserDummie(uid=7, login='Shanya', password='Yanix', nickname='YandexTop'),
    UserDummie(uid=8, login='Andrew', password='Yanix',
               nickname='Xo4Y_V_YanDex')]

_TASKS = [
    TaskDummie(uid=1, creator_uid=1, tid=1, deadline=None, title='tesg task'),
    TaskDummie(uid=1, creator_uid=1, tid=2, deadline=None, title='tesg task 1',
               parent=1),
    TaskDummie(uid=1, creator_uid=1, priority=Priority.HIGH, tid=3,
               deadline=222222222222, title='test task 2', parent=1),
    TaskDummie(uid=1, creator_uid=1, tid=4, deadline=None, title='test task 3'),
    TaskDummie(uid=2, creator_uid=2, tid=5, deadline=None, title='test task 4'),
    TaskDummie(uid=2, creator_uid=2, tid=6, deadline=None, title='test task 5'),
    TaskDummie(uid=2, creator_uid=2, tid=7, deadline=2321, title='test task 6'),
    TaskDummie(uid=2, creator_uid=2, tid=8, deadline=1233321,
               title='test task 7'),
    TaskDummie(uid=1, creator_uid=1, tid=9, deadline=500000000,
               title='test task 8', parent=3),
    TaskDummie(uid=1, creator_uid=1, tid=10, deadline=None, title='test task 9',
               parent=2),
    TaskDummie(uid=1, creator_uid=1, tid=11, deadline=None,
               title='test task 10', parent=9)]

_PROJECTS = [
    ProjectDummie(pid=1, admin_uid=1, title='project 1', description='Huh?'),
    ProjectDummie(pid=2, admin_uid=1, title='project 2',
                  description='this is siiiiper cool'),
    ProjectDummie(pid=3, admin_uid=2, title='project 3',
                  description='Some unit test?'),
    ProjectDummie(pid=4, admin_uid=2, title='project 4', description='0_0')]

_USER_PROJECT_RELATIONS = [{'user_id': 2, 'project_id': 1},
                           {'user_id': 3, 'project_id': 1},
                           {'user_id': 5, 'project_id': 1},
                           {'user_id': 5, 'project_id': 2},
                           {'user_id': 4, 'project_id': 3},
                           {'user_id': 5, 'project_id': 3},
                           {'user_id': 3, 'project_id': 3},
                           {'user_id': 1, 'project_id': 3}]

_PROJECT_TASKS = [TaskDummie(uid=2, creator_uid=1, tid=12, pid=1, deadline=None,
                             title='test pr 1'),
                  TaskDummie(uid=2, creator_uid=1, tid=13, pid=1, deadline=None,
                             title='test pr 2'),
                  TaskDummie(uid=1, creator_uid=1, tid=14, pid=1, deadline=None,
                             title='test pr 3'),
                  TaskDummie(uid=3, creator_uid=1, tid=15, pid=1, deadline=None,
                             title='test pr 4', priority=Priority.MIN),
                  TaskDummie(uid=1, creator_uid=1, tid=16, pid=2, deadline=None,
                             title='test pr 5'),
                  TaskDummie(uid=5, creator_uid=1, tid=17, pid=2, deadline=None,
                             title='test pr 6'),
                  TaskDummie(uid=5, creator_uid=1, tid=18, pid=2, deadline=None,
                             title='test pr 7'),
                  TaskDummie(uid=1, creator_uid=1, tid=19, pid=2, deadline=None,
                             title='test pr 8'),
                  TaskDummie(uid=1, creator_uid=2, tid=20, pid=3, deadline=None,
                             title='test pr 9'),
                  TaskDummie(uid=2, creator_uid=2, tid=21, pid=3, deadline=None,
                             title='test pr 10'),
                  TaskDummie(uid=3, creator_uid=2, tid=22, pid=3, deadline=None,
                             title='test pr 11'),
                  TaskDummie(uid=4, creator_uid=2, tid=23, pid=3, deadline=None,
                             title='test pr 12'),
                  TaskDummie(uid=2, creator_uid=2, tid=24, pid=4, deadline=None,
                             title='test pr 13'),
                  TaskDummie(uid=2, creator_uid=2, tid=25, pid=4, deadline=None,
                             title='test pr 14')]


def _init_user_table():
    for user in _USERS:
        User.create(login=user.login,
                    nickname=user.nickname,
                    password=user.password)


def _init_task_table():
    for task in _TASKS:
        Task.create(creator=task.creator_uid,
                    receiver=task.uid,
                    project=task.pid,
                    status=task.status,
                    parent=task.parent,
                    title=task.title,
                    priority=task.priority,
                    deadline_time=task.deadline,
                    comment=task.comment,
                    realization_time=task.realization_time,
                    creation_time=task.creation_time)


def _init_project_table():
    for project in _PROJECTS:
        print(project.admin_uid)
        Project.create(admin=project.admin_uid,
                       description=project.description,
                       title=project.title)

        UserProjectRelation.create(user=project.admin_uid,
                                   project=project.pid)

    # add another members relations
    for relation in _USER_PROJECT_RELATIONS:
        UserProjectRelation.create(user=relation['user_id'],
                                   project=relation['project_id'])


# need for _init_task_table
def _init_project_tasks_table():
    for task in _PROJECT_TASKS:
        Task.create(creator=task.creator_uid,
                    receiver=task.uid,
                    project=task.pid,
                    status=task.status,
                    parent=task.parent,
                    title=task.title,
                    priority=task.priority,
                    deadline_time=task.deadline,
                    comment=task.comment,
                    realization_time=task.realization_time,
                    creation_time=task.creation_time
                    )
