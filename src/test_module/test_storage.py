import unittest
from storage.adapter_classes import Task, User, Project, UserProjectRelation
from storage.project_adapter import ProjectAdapter
from storage.user_adapter import UserAdapter
from storage.task_adapter import TaskAdapter

_USERS = {'sanya': {'pid': 1, 'password': '12345', 'nickname': 'sanya'},
          'vasya': {'pid': 2, 'password': '12345', 'nickname': 'Vasyanya'},
          'shAfT': {'pid': 3, 'password': '54321', 'nickname': 'Boudart'},
          'Andrew': {'pid': 4, 'password': 'weratt', 'nickname': 'Andy'},
          'sudouser228': {'pid': 5, 'password': '1111', 'nickname': 'Hehehe'}}

_TASKS = {'test task': {'receiver': 1, 'creator': 1, 'project': None,
                        'status': 2, 'priority': 2, 'parent': None,
                        'deadline_time': None, 'comment': '', 'tid': 1},
          'test task 2': {'receiver': 1, 'creator': 1, 'project': None,
                          'status': 2, 'priority': 2, 'parent': None,
                          'deadline_time': None, 'comment': '', 'tid': 2},
          'test task 3': {'receiver': 1, 'creator': 1, 'project': None,
                          'status': 1, 'priority': 1, 'parent': None,
                          'deadline_time': None, 'comment': '', 'tid': 3},
          'test task 4': {'receiver': 2, 'creator': 2, 'project': None,
                          'status': 3, 'priority': 3, 'parent': None,
                          'deadline_time': None, 'comment': '', 'tid': 4},
          'test task 5': {'receiver': 2, 'creator': 2, 'project': None,
                          'status': 2, 'priority': 2, 'parent': None,
                          'deadline_time': 15000000, 'comment': '', 'tid': 5},
          'test task 6': {'receiver': 1, 'creator': 1, 'project': None,
                          'status': 2, 'priority': 2, 'parent': 1,
                          'deadline_time': None, 'comment': '', 'tid': 6},
          'test task 7': {'receiver': 1, 'creator': 1, 'project': None,
                          'status': 2, 'priority': 2, 'parent': 1,
                          'deadline_time': 121, 'comment': '', 'tid': 7},
          'test task 8': {'receiver': 1, 'creator': 1, 'project': None,
                          'status': 2, 'priority': 2, 'parent': 7,
                          'deadline_time': None, 'comment': '', 'tid': 8},
          'test task 9': {'receiver': 1, 'creator': 1, 'project': 1,
                          'status': 2, 'priority': 2, 'parent': None,
                          'deadline_time': None, 'comment': '', 'tid': 9},
          'test task 10': {'receiver': 1, 'creator': 1, 'project': 1,
                           'status': 2, 'priority': 2, 'parent': 9,
                           'deadline_time': None, 'comment': '', 'tid': 10},
          'test task 11': {'receiver': 1, 'creator': 1, 'project': 1,
                           'status': 2, 'priority': 2, 'parent': 10,
                           'deadline_time': None, 'comment': '', 'tid': 11},
          'test task 12': {'receiver': 1, 'creator': 1, 'project': 1,
                           'status': 2, 'priority': 2, 'parent': 7,
                           'deadline_time': None, 'comment': '', 'tid': 12}
          }

_PROJECTS = {'project 1': {'admin': 1, 'description': 'project', 'pid': 1},
             'project 2': {'admin': 1, 'description': 'proJECT', 'pid': 2},
             'project 3': {'admin': 2, 'description': 'project', 'pid': 3}}

_USER_PROJECT_RELATIONS = [{'pid': 1, 'uid': 1}, {'pid': 2, 'uid': 1},
                           {'pid': 3, 'uid': 2}]


def _init_user_table():
    for login, params in _USERS.items():
        User.create(login=login,
                    nickname=params['nickname'],
                    password=params['password'])


def _init_task_table():
    for title, params in _TASKS.items():
        Task.create(creator=params['creator'],
                    receiver=params['receiver'],
                    project=params['project'],
                    status=params['status'],
                    parent=params['parent'],
                    title=title,
                    priority=params['priority'],
                    deadline_time=params['deadline_time'],
                    comment=params['comment'])


def _init_project_table():
    for title, params in _PROJECTS.items():
        Project.create(admin=params['admin'],
                       description=params['description'],
                       title=title)

        UserProjectRelation.create(user=params['admin'],
                                   project=params['pid'])


class TestTaskAdapter(unittest.TestCase):

    def setUp(self):
        self.project_adapter = ProjectAdapter(db_name='memory:')
        _init_project_table()
        _init_task_table()
        _init_user_table()

    def test_add_project(self):
        self.assertEqual(1, 1)
