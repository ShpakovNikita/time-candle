from datetime import time

from tests import *
from time_candle.controller.commands import Controller
from time_candle.model.tokenizer import parse_string
import time_candle.exceptions.show_me_exceptions as sm_e
import time_candle.exceptions.model_exceptions as m_e
import time_candle.model.time_formatter as formatter


# TODO: Mock. It is really hard to implement here. Like very-very-very hard.
# Assume that we tested or storage module very well


class TestTaskLogic(unittest.TestCase):
    # Note that we also testing our tokenizer

    def _change_user(self, uid):
        self.controller.task_logic._auth(_USERS[uid - 1].uid)
        self.controller.project_logic._auth(_USERS[uid - 1].uid)

    def setUp(self):
        self.controller = Controller(db_file=db_file)

        _init_project_table()

    def tearDown(self):
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_simple_add_get_task(self):
        self._change_user(_USERS[0].uid)
        # check that we can add tasks
        self.assertEqual(len(self.controller.get_tasks('')), 0)
        self.controller.add_task(
            'asd', None, None, None, None, '', None, None, None)
        self.assertEqual(len(self.controller.get_tasks('')), 1)

        # check that we do not have rights to see user's tasks
        self._change_user(_USERS[1].uid)
        self.assertEqual(len(self.controller.get_tasks('')), 0)

        # remove not ours task
        self._change_user(_USERS[0].uid)
        self.controller.remove_task(1)
        self.assertEqual(len(self.controller.get_tasks('')), 0)

    def test_primary_get_by_filter(self):
        _init_task_table()
        _init_project_tasks_table()

        self._change_user(_USERS[0].uid)
        # let's test our filter tokenizer
        self.assertEqual(len(self.controller.get_tasks('')), 19)
        self.assertEqual(len(self.controller.get_tasks(
            'projects: None')), 7)
        self.assertEqual(len(self.controller.get_tasks(
            'projects: None AND titles: tesg 3')), 3)
        self.assertEqual(len(self.controller.get_tasks(
            'projects: None AND titles: tesg 4')), 2)

        self.assertEqual(
            len(self.controller.get_tasks(
                '(projects: None AND titles: tesg 3) OR tids: 9 10')), 5)
        self.assertEqual(
            len(self.controller.get_tasks(
                '(projects:  None AND titles: tesg 3) OR tids: 9 4')), 4)
        self.assertEqual(
            len(self.controller.get_tasks(
                '(projects: None OR projects: 1) AND titles: pr')), 4)
        self.assertEqual(
            len(self.controller.get_tasks(
                '(projects: None OR projects: 1) AND (titles: pr)')), 4)
        self.assertEqual(
            len(self.controller.get_tasks(
                '(projects: None OR projects: 1) AND (titles: pr OR tids: 1 2)')
                ), 6)

        # relog test
        self._change_user(_USERS[1].uid)
        self.assertNotEqual(
            len(self.controller.get_tasks(
                '(projects: None AND titles: tesg 3) OR tids: 9 10')), 5)

        # check it on the error situations
        with self.assertRaises(sm_e.InvalidExpressionError):
            self.controller.get_tasks('dsa')

        with self.assertRaises(sm_e.InvalidExpressionError):
            self.controller.get_tasks('projects: dsa 2 3')

        with self.assertRaises(sm_e.InvalidExpressionError):
            self.controller.get_tasks('projects: 1 2 3 AND OR projects: 2 3')

        with self.assertRaises(sm_e.InvalidExpressionError):
            self.controller.get_tasks('projects: 1 2 3 AND ()')

    def test_add_validations(self):
        pass

    def test_period_tasks(self):
        pass

    def test_time_get_by_filter_tasks(self):
        pass

    def test_add_get_priority_depth_dependency(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)

        self.controller.change_task(_TASKS[0].tid, priority=Priority.HIGH)
        task_9 = self.controller.get_tasks('tids: ' + str(_TASKS[8].tid))[0]
        self.assertLessEqual(task_9.priority, Priority.HIGH)

        self.controller.change_task(_TASKS[0].tid, priority=Priority.LOW)
        task_9 = self.controller.get_tasks('tids: ' + str(_TASKS[8].tid))[0]
        self.assertLessEqual(task_9.priority, Priority.HIGH)

        self.controller.change_task(_TASKS[0].tid, priority=Priority.MAX)
        task_9 = self.controller.get_tasks('tids: ' + str(_TASKS[8].tid))[0]
        self.assertLessEqual(task_9.priority, Priority.MAX)

    def test_add_get_priority_dependency(self):
        self._change_user(_USERS[0].uid)

        self.controller.add_task(title=_TASKS[0].title,
                                 priority=_TASKS[0].priority,
                                 parent_id=_TASKS[0].parent)
        self.controller.change_task(_TASKS[0].tid, priority=Priority.HIGH)
        self.controller.add_task(title=_TASKS[1].title,
                                 priority=Priority.MEDIUM,
                                 parent_id=_TASKS[1].parent)

        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[1].tid))[0]
        self.assertEqual(task_1.priority, Priority.HIGH)

        self.controller.change_task(_TASKS[0].tid, priority=Priority.MEDIUM)
        # update out task
        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[1].tid))[0]
        self.assertEqual(task_1.priority, Priority.HIGH)

        self.controller.change_task(_TASKS[0].tid, priority=Priority.MAX)
        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[1].tid))[0]
        self.assertEqual(task_1.priority, Priority.MAX)

    def test_add_change_done_status_dependency(self):
        self._change_user(_USERS[0].uid)

        self.controller.add_task(title=_TASKS[0].title,
                                 status=_TASKS[0].status,
                                 parent_id=_TASKS[0].parent)
        self.controller.change_task(_TASKS[0].tid, status=Status.DONE)

        # check that we cannot make child to the done task
        with self.assertRaises(m_e.InvalidStatusError):
            self.controller.add_task(title=_TASKS[1].title,
                                     status=_TASKS[1].status,
                                     parent_id=_TASKS[1].parent)

        # after changing the status we may do this
        self.controller.change_task(_TASKS[0].tid, status=Status.IN_PROGRESS)
        self.controller.add_task(title=_TASKS[1].title,
                                 status=_TASKS[1].status,
                                 parent_id=_TASKS[1].parent)

    def test_change_task_deadline(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)
        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[0].tid))[0]

        self.assertEqual(task_1.deadline, None)

        # far-far future
        self.controller.change_task(1, time='2077-07-20 21:29:00')
        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[0].tid))[0]

        self.assertNotEqual(task_1.deadline, None)

    # this test tests that childs will become also expired if not done due to
    # their parent expiration
    def test_change_expired_status_dependency(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)

        with self.assertRaises(m_e.InvalidTimeError):
            self.controller.change_task(1, status=Status.EXPIRED)

        self.controller.change_task(1, time='2077-01-01 20:00:00')
        task_1 = self.controller.get_tasks('tids: ' + str(_TASKS[0].tid))[0]
        print('desu!', task_1.deadline)
        self.controller.change_task(1, status=Status.EXPIRED)

    def test_change_status_dependency(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)

        # check that due to dependencies we cannot do our tasks
        with self.assertRaises(m_e.InvalidStatusError):
            self.controller.change_task(1, status=Status.DONE)
            self.controller.change_task(3, status=Status.DONE)
            self.controller.change_task(9, status=Status.DONE)

        # by the chain from lowest levels we will do them
        # tid 3 chain:
        self.controller.change_task(11, status=Status.DONE)
        self.controller.change_task(9, status=Status.DONE)
        self.controller.change_task(3, status=Status.DONE)

        # tid 2 chain:
        self.controller.change_task(10, status=Status.DONE)
        self.controller.change_task(2, status=Status.DONE)

        # tid 1 main do:
        self.controller.change_task(1, status=Status.DONE)

    def test_child_get_tasks(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)

        selected_tasks = self.controller.get_tasks('')

        # we have to be 100% sure that we are getting proper tasks
        task_1 = next(filter(lambda t: t.tid == 1, selected_tasks))
        task_2 = next(filter(lambda t: t.tid == 2, selected_tasks))
        task_3 = next(filter(lambda t: t.tid == 3, task_1.childs))

        self.assertEqual(len(task_1.childs), 2)
        self.assertEqual(len(task_2.childs), 1)

        # 2 layout of depth test
        self.assertEqual(len(task_3.childs), 1)

        task_12 = next(filter(lambda t: t.tid == 12, selected_tasks))
        task_13 = next(filter(lambda t: t.tid == 13, selected_tasks))

        self.assertEqual(len(task_12.childs), 1)
        self.assertEqual(len(task_13.childs), 0)

        self._change_user(_USERS[2].uid)

        task_12 = next(filter(lambda t: t.tid == 12, selected_tasks))
        task_13 = next(filter(lambda t: t.tid == 13, selected_tasks))

        self.assertEqual(len(task_12.childs), 1)
        self.assertEqual(len(task_13.childs), 0)

    def test_union(self):
        fil_1 = TaskFilter().to_query()
        self.assertEqual(parse_string('').to_query(), fil_1)


class TestFormatting(unittest.TestCase):
    def test_days_milliseconds_formatting(self):
        ms = formatter.days_to_milliseconds(1)
        self.assertEqual(ms, 1 * 24 * 60 * 60 * 1000)

        days = formatter.milliseconds_to_days(ms)
        self.assertEqual(1, 1)

    def test_datetime_milliseconds_formatting(self):
        pass