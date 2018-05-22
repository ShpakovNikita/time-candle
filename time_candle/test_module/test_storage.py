from test_module import *


TEST_DB = ':memory:'


class TestTaskAdapter(unittest.TestCase):

    def setUp(self):
        self.adapter = TaskAdapter(db_name=TEST_DB)
        _init_project_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_save_get_task(self):
        # trying to add task to the None user and creator. This tests if the
        # exception is raised when our id is invalid
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

        self.adapter.uid = 2

        # test that when we switch user we will ignore tid and make new task
        task = copy(_TASKS[5])
        task.tid = 3
        self.adapter.save(task)
        self.adapter.save(task)
        self.assertEqual(self.adapter.last_id(), 3)

        self.adapter.uid = 1
        self.adapter.save(task)
        self.assertEqual(self.adapter.last_id(), 4)

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

        # checking that we cannot remove deleted task somehow twice
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
        self.assertEqual(self.adapter.last_id(), 0)

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
        self.adapter = UserAdapter(db_name=TEST_DB)
        _init_task_table()
        _init_project_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_add_user(self):
        self.adapter.save(_USERS[0])

        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.save(_USERS[0])

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

    def test_remove_get_by_project(self):
        _init_user_table()

        # check our function on correct by length
        self.adapter.uid = 1
        self.assertEqual(len(self.adapter.get_by_project(1)), 4)

        # remove element and test again
        self.adapter.remove_from_project_by_login('Shaft', 1)
        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.remove_from_project_by_login('Andy', 1)

        result = self.adapter.get_by_project(1)
        self.assertEqual(len(result), 3)
        self.assertEqual(len(self.adapter.get_by_project(2)), 2)

        # if the uid is invalid...
        self.adapter.uid = None
        with self.assertRaises(db_e.InvalidUidError):
            self.adapter.get_by_project(1)

        # if there is no such project to this user
        self.adapter.uid = 7
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.get_by_project(1)

        self.adapter.uid = 3
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.get_by_project(2)

        for user in result:
            self.assertIn(user.uid, [3, 5, 1])

    def test_get_filter(self):
        _init_user_table()

        # let's test search filters
        self.assertEqual(len(self.adapter.get_by_filter(
            UserFilter().login_substring(r'sa'))), 3)
        self.assertEqual(len(self.adapter.get_by_filter(
            UserFilter().login_substring(r'san'))), 2)
        self.assertEqual(len(self.adapter.get_by_filter(
            UserFilter().nickname_substring(r'Sa'))), 3)

        # test union filter
        self.assertEqual(len(self.adapter.get_by_filter(UserFilter())), 8)

        # test complex filters
        res_1, res_2 = 2, 3
        fil_1 = UserFilter().login_substring(r'sa').nickname_substring(r'Sa')
        self.assertEqual(len(self.adapter.get_by_filter(fil_1)), res_1)

        fil_2 = UserFilter().login_substring(r'Sha'). \
            nickname_substring(r'BPA', PrimaryFilter.OP_OR)
        self.assertEqual(len(self.adapter.get_by_filter(fil_2)), res_2)

        users = self.adapter.get_by_filter(fil_1 | fil_2)
        self.assertEqual(len(users),
                         res_2 + res_1)
        self.assertEqual(len(self.adapter.get_by_filter(fil_1 & fil_2)),
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
    def setUp(self):
        self.adapter = ProjectAdapter(db_name=TEST_DB)
        _init_task_table()
        _init_project_tasks_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_get_save_project(self):
        # trying to add project with None admin.
        with self.assertRaises(db_e.InvalidLoginError):
            project = copy(_PROJECTS[0])
            project.admin_uid = self.adapter.uid
            self.adapter.save(project)

        # check that there is no projects in database
        self.assertEqual(self.adapter.last_id(), 0)

        self.adapter.uid = 1
        self.adapter.save(_PROJECTS[0])
        self.assertEqual(self.adapter.last_id(), 1)

        # check that project was updated
        project = copy(_PROJECTS[0])
        project.description = 'new_desc'
        self.adapter.save(project)
        self.assertEqual(self.adapter.last_id(), 1)

        self.assertEqual(self.adapter.get_project_by_id(_PROJECTS[0].pid).
                         description, project.description)

        # check if we can remove project
        self.adapter.remove_project_by_id(_PROJECTS[0].pid)

        self.assertEqual(self.adapter.last_id(), 0)

        # check on correct addition to the db after all
        self.adapter.save(_PROJECTS[0])
        self.adapter.save(_PROJECTS[1])
        self.assertEqual(self.adapter.last_id(), 2)

        self.adapter.uid = 2
        # check that we cannot delete project if we are not admins
        with self.assertRaises(db_e.InvalidLoginError):
            self.adapter.remove_project_by_id(_PROJECTS[0].pid)

        # check on the right message if we delete unexistent project
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.remove_project_by_id(100)

    def test_remove_task_project(self):
        _init_project_table()

        self.adapter.uid = 1
        self.adapter.remove_project_by_id(_PROJECTS[0].pid)

        # check that all tasks was removed
        tasks = [project_task.tid for project_task in _PROJECT_TASKS
                 if project_task.pid == _PROJECTS[0].pid]

        for task in Task.select().where(Task.tid.is_null(False)):
            self.assertNotIn(task.tid, tasks)

        # check just for sure that we do not deleted some other task
        Task.select().where(Task.tid == 20).get()

        # check that all relations between _PROJECT[0] was removed
        with self.assertRaises(db_e.InvalidPidError):
            self.adapter.get_project_by_id(_PROJECTS[0].pid)

        for rel in UserProjectRelation.select().where(
                UserProjectRelation.project.is_null(False)):
            self.assertNotEqual(rel.project.pid, _PROJECTS[0].pid)

    def test_get_by_filter(self):
        _init_project_table()

        self.adapter.uid = 1
        # let's test search filters
        self.assertEqual(len(self.adapter.get_by_filter(
            ProjectFilter().description_substring(r'u'))), 2)
        self.assertEqual(len(self.adapter.get_by_filter(
            ProjectFilter().description_substring(r'Huh'))), 1)

        self.adapter.uid = None
        # test union filter
        self.assertEqual(len(self.adapter.get_by_filter(ProjectFilter())), 0)

        self.adapter.uid = 1
        self.assertEqual(len(self.adapter.get_by_filter(ProjectFilter())), 3)

        res_1, res_2 = 2, 3
        # analogue to the union
        fil_1 = ProjectFilter().admin(1)
        self.assertEqual(len(self.adapter.get_by_filter(fil_1)), res_1)

        fil_2 = ProjectFilter().description_substring(r'u'). \
            description_substring(r'iii', PrimaryFilter.OP_OR)
        self.assertEqual(len(self.adapter.get_by_filter(fil_2)), res_2)

        self.assertEqual(len(self.adapter.get_by_filter(fil_1 | fil_2)), 3)

        projects = self.adapter.get_by_filter(fil_1 & fil_2)
        self.assertEqual(len(projects), 2)

        # now we check the truth of the gotten values
        for project in projects:
            self.assertIn(project.pid, [1, 2])
