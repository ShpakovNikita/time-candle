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
    UserDummie(uid=5, login='sanga', password='Yanix', nickname='BPATUIIIKA'),
    UserDummie(uid=6, login='Sashya', password='Ya', nickname='SanEk'),
    UserDummie(uid=7, login='Shanya', password='Yanix', nickname='YandexTop'),
    UserDummie(uid=8, login='Andrew', password='Yanix',
               nickname='Xo4Y_V_YanDex')]

_TASKS = [
    TaskDummie(uid=1, creator_uid=1, tid=1, deadline=None, title='test task'),
    TaskDummie(uid=1, creator_uid=1, tid=2, deadline=None, title='test task 1',
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
    ProjectDummie(pid=2, admin_uid=1, title='project 2'),
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
                    comment=task.comment)


def _init_project_table():
    for project in _PROJECTS:
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
                    comment=task.comment)


class TestTaskAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = TaskAdapter(db_name=':memory:')
        _init_project_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_save_get_task(self):
        # trying to add task to the None user and creator. This tests if the
        # exception is rised when our id is invalid
        with self.assertRaises(db_e.InvalidLoginError):
            task = copy(_TASKS[0])
            # Uid None
            task.uid = self.adapter.uid
            self.adapter.save(task)

        with self.assertRaises(db_e.InvalidLoginError):
            task = copy(_TASKS[1])
            # Uid None
            task.creator_uid = self.adapter.uid
            self.adapter.save(task)

        # this tests if we can't create two equal by tid tasks (it has to update
        # them)

        # first we have to log in
        self.adapter.uid = 1

        # check that the no tasks has 0 id
        self.assertEqual(self.adapter.last_id(), 0)

        self.adapter.save(_TASKS[0])
        self.adapter.save(_TASKS[0])

        # check that we updated task
        self.assertEqual(self.adapter.last_id(), 1)

        task = copy(_TASKS[0])
        task.tid = self.adapter.last_id() + 1
        self.adapter.save(task)

        # check that we created task
        self.assertEqual(self.adapter.last_id(), 2)

    def test_get_by_filter_task(self):
        _init_task_table()
        _init_project_tasks_table()

        self.adapter.uid = 1

        fil = TaskFilter()
        # test union filter
        self.assertEqual(len(self.adapter.get_by_filter(fil)), 19)

        fil.priority(Priority.MEDIUM, TaskFilter.OP_GREATER)
        # all tasks with priority greater then medium
        self.assertEqual(len(self.adapter.get_by_filter(fil)), 1)

        fil_2 = TaskFilter()
        fil_2.priority(Priority.MEDIUM, TaskFilter.OP_LESS)

        # all tasks with priority greater then medium or less then medium
        # (not equals medium)
        self.assertEqual(len(self.adapter.get_by_filter(fil | fil_2)), 2)

        fil.priority(Priority.MEDIUM, TaskFilter.OP_LESS, PrimaryFilter.OP_OR)
        self.assertEqual(len(self.adapter.get_by_filter(fil)), 2)

        fil = TaskFilter()
        fil.priority(Priority.MEDIUM, TaskFilter.OP_NOT_EQUALS)
        self.assertEqual(len(self.adapter.get_by_filter(fil)), 2)

        # trying to take some more complex filter with lists
        tasks = self.adapter.get_by_filter(
            TaskFilter().project([1, 3]).receiver([2, 1]))
        self.assertEqual(len(tasks), 5)

        # check on assertations
        with self.assertRaises(db_e.InvalidFilterOperator):
            TaskFilter().priority(Priority.MEDIUM, TaskFilter.OP_NOT_EQUALS + 1)

        # we check our result on length, but we have also to check if they are
        # right
        for task in tasks:
            self.assertIn(task.tid, [12, 13, 14, 20, 21])

        # little tests for get_by_id function
        self.assertEqual(self.adapter.get_task_by_id(3).tid, 3)
        self.assertEqual(self.adapter.get_task_by_id(3).title, 'test task 2')

        with self.assertRaises(db_e.InvalidTidError):
            self.adapter.get_task_by_id(100)

        with self.assertRaises(db_e.InvalidTidError):
            self.adapter.get_task_by_id(5)

    def test_remove_save_get_task(self):
        # adding tasks
        for i in range(4):
            self.adapter.save(_TASKS[i])

        self.adapter.uid = 1
        # remove the 4th task
        self.adapter.remove_task_by_id(_TASKS[3].tid)

        # checking tha we cannot remove deleted task somehow twice
        with self.assertRaises(db_e.InvalidTidError):
            self.adapter.remove_task_by_id(_TASKS[3].tid)

        self.adapter.uid = 2

        # check that we cannot remove not our task
        with self.assertRaises(db_e.InvalidTidError):
            self.adapter.remove_task_by_id(_TASKS[1].tid)

        self.adapter.uid = 1
        # delete childs recursive
        self.adapter.remove_task_by_id(_TASKS[0].tid)

        # check if we are really deleted them
        self.assertEqual(len(self.adapter.get_by_filter(TaskFilter())), 0)

        _init_task_table()
        _init_project_tasks_table()

        # check all above but on the project tasks
        with self.assertRaises(db_e.InvalidTidError):
            self.adapter.remove_task_by_id(24)

        self.adapter.remove_task_by_id(13)

        self.adapter.uid = 2
        self.adapter.remove_task_by_id(25)


class TestUserAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = UserAdapter(db_name=':memory:')
        _init_task_table()
        _init_project_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_add_user(self):
        self.adapter.add_user(_USERS[0].login, _USERS[0].password)

        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.add_user(_USERS[0].login, _USERS[0].password)

        for user in _USERS[1:]:
            User.create(login=user.login,
                        nickname=user.nickname,
                        password=user.password)

        # check all add to project situations

        # try to add user from non admin
        self.adapter.uid = 1
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.add_user_to_project_by_id(_USERS[0].login, 4)

        # add user from admin
        self.adapter.uid = 2
        self.adapter.add_user_to_project_by_id(_USERS[0].login, 4)

        # add the same user twice
        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.add_user_to_project_by_id(_USERS[0].login, 4)

        # check that we cannot add other users even when we are in project, but
        # not admins
        self.adapter.uid = 1
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.add_user_to_project_by_id(_USERS[2].login, 4)

    def test_login(self):
        _init_user_table()
        self.adapter.login_user(_USERS[0].login, _USERS[0].password)
        self.adapter.login_user(_USERS[0].login, _USERS[0].password)

        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.login_user('tochno_sanya', _USERS[0].password)

        with self.assertRaises(db_e.InvalidPasswordError):
            self.adapter.login_user(_USERS[0].login, _USERS[1].password)

    def test_get_by_uid_login(self):
        _init_user_table()

        # if we got right id
        self.assertEqual(self.adapter.get_id_by_login(_USERS[0].login),
                         _USERS[0].uid)

        # what if we get unexistent user
        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.get_id_by_login('hahahaha')

        # test get by id
        self.assertEqual(self.adapter.get_user_by_id(_USERS[2].uid).nickname,
                         _USERS[2].nickname)

        with self.assertRaises(db_e.InvalidUidError):
            self.adapter.get_user_by_id(100)

    def test_get_filter(self):
        _init_user_table()

        # let's test search filters
        self.assertEqual(len(self.adapter.get_users_by_filter(
            UserFilter().login_substring(r'sa'))), 3)
        self.assertEqual(len(self.adapter.get_users_by_filter(
            UserFilter().login_substring(r'san'))), 2)
        self.assertEqual(len(self.adapter.get_users_by_filter(
            UserFilter().nickname_substring(r'Sa'))), 3)

        # test union filter
        self.assertEqual(len(self.adapter.get_users_by_filter(UserFilter())), 8)

        # test complex filters
        res_1, res_2 = 2, 3
        fil_1 = UserFilter().login_substring(r'sa').nickname_substring(r'Sa')
        self.assertEqual(len(self.adapter.get_users_by_filter(fil_1)), res_1)

        fil_2 = UserFilter().login_substring(r'Sha').\
            nickname_substring(r'BPA', PrimaryFilter.OP_OR)
        self.assertEqual(len(self.adapter.get_users_by_filter(fil_2)), res_2)

        users = self.adapter.get_users_by_filter(fil_1 | fil_2)
        self.assertEqual(len(users),
                         res_2 + res_1)
        self.assertEqual(len(self.adapter.get_users_by_filter(fil_1 & fil_2)),
                         0)

        # we check our result on length, but we have also to check if they are
        # right
        for user in users:
            self.assertIn(user.uid, [1, 2, 5, 6, 7])

    def test_in_remove_from_project(self):
        _init_user_table()

        self.adapter.is_user_in_project(_USERS[0].login, 3)

        # if the user is not in project
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.is_user_in_project(_USERS[0].login, 4)

        # if the pid is invalid...
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.is_user_in_project(_USERS[0].login, 10)

        self.adapter.uid = 2

        self.adapter.remove_from_project_by_login(_USERS[0].login, 3)

        # remove removed user in project
        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.remove_from_project_by_login(_USERS[0].login, 3)

        # remove admin from the project with no rights
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.remove_from_project_by_login(_USERS[0].login, 2)

        self.adapter.uid = 1

        # remove admin from the project with rights
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.remove_from_project_by_login(_USERS[0].login, 2)

        # try to remove myself when I'm not admin
        self.adapter.uid = 2
        self.adapter.remove_from_project_by_login(_USERS[1].login, 1)


class TestProjectAdapter(unittest.TestCase):
    pass
