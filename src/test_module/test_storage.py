import unittest
from storage.adapter_classes import Task, User, Project, UserProjectRelation
from storage.project_adapter import ProjectAdapter
from storage.user_adapter import UserAdapter
from storage.task_adapter import TaskAdapter
from enums.priority import Priority
from enums.status import Status
import exceptions.db_exceptions as db_e


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
               realization_time=-1):
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


TaskDummie = type('TaskDummie', (), {'__init__': _task_init})


# User dummie.
def _user_init(self,
               uid=None,
               login='guest',
               password=None,
               time_zone=None,
               nickname='guest',
               about=''):
    self.uid = uid
    self.login = login
    self.nickname = nickname
    self.password = password
    self.time_zone = time_zone
    self.about = about


UserDummie = type('UserDummie', (), {'__init__': _user_init})

_USERS = [
    UserDummie(uid=1, login='sanya', password='12345', nickname='SaNo228'),
    UserDummie(uid=2, login='Shaft', password='123', nickname='SaNo228'),
    UserDummie(uid=3, login='Arracias', password='12345', nickname='Boudart'),
    UserDummie(uid=4, login='Andy', password='123452', nickname='weratt'),
    UserDummie(uid=5, login='Vasya', password='Yanix', nickname='BPATUIIIKA')]

_TASKS = [
    TaskDummie(uid=1, creator_uid=1, tid=1, deadline=None, title='test task'),
    TaskDummie(uid=1, creator_uid=1, tid=2, deadline=None, title='test task 1'),
    TaskDummie(uid=1, creator_uid=1, tid=3, deadline=222222222222,
               title='test task 2'),
    TaskDummie(uid=1, creator_uid=1, tid=4, deadline=None, title='test task 3'),
    TaskDummie(uid=2, creator_uid=2, tid=5, deadline=None, title='test task 4'),
    TaskDummie(uid=2, creator_uid=2, tid=6, deadline=None, title='test task 5'),
    TaskDummie(uid=2, creator_uid=2, tid=7, deadline=2321, title='test task 6'),
    TaskDummie(uid=2, creator_uid=2, tid=8, deadline=1233321,
               title='test task 7'),
    TaskDummie(uid=1, creator_uid=1, tid=9, deadline=500000000,
               title='test task 8'),
    TaskDummie(uid=1, creator_uid=1, tid=10, deadline=None, title='test task 9',
               parent=2),
    TaskDummie(uid=1, creator_uid=1, tid=11, deadline=None,
               title='test task 10', parent=10)
]

_PROJECTS = [
    ProjectDummie(pid=1, admin_uid=1, title='project 1', description='Huh?'),
    ProjectDummie(pid=2, admin_uid=1, title='project 2'),
    ProjectDummie(pid=3, admin_uid=2, title='project 3',
                  description='Some unit test?'),
    ProjectDummie(pid=4, admin_uid=2, title='project 4', description='0_0')]


def _init_user_table():
    for user in _USERS:
        print(user.login,
              user.nickname,
              user.password)
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
                    comment=task.comment)


def _init_project_table():
    for project in _PROJECTS:
        Project.create(admin=project.admin_uid,
                       description=project.description,
                       title=project.title)

        UserProjectRelation.create(user=project.admin_uid,
                                   project=project.pid)


class TestTaskAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = TaskAdapter(db_name=':memory:')
        _init_project_table()
        # _init_task_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_add_task(self):

        # Trying to add task to the None user and creator
        with self.assertRaises(db_e.InvalidLoginError):
            task_1 = _TASKS[0]
            # Uid None
            task_1.uid = self.adapter.uid
            self.adapter.save(task_1)

            task_2 = _TASKS[1]
            # Uid None
            task_2.creator_uid = self.adapter.uid
            self.adapter.save(task_2)

        self.adapter.uid = 1

        self.assertEqual(1, 1)

    def test_heh_huh(self):
        self.assertEqual(1, 1)


class TestUserAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = UserAdapter(db_name=':memory:')

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_add_user(self):
        # Not raises
        self.adapter.add_user(_USERS[0].login, _USERS[0].password)

        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.add_user(_USERS[0].login, _USERS[0].password)
