from tests import *
from time_candle.controller.commands import Controller
from time_candle.model.tokenizer import parse_string
import time_candle.exceptions.show_me_exceptions as sm_e


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

    def test_child_get_tasks(self):
        _init_task_table()
        _init_project_tasks_table()
        self._change_user(_USERS[0].uid)

        selected_tasks = self.controller.get_tasks('')

        # we have to be 100% sure that we are getting proper tasks
        task_1 = next(filter(lambda t: t.tid == 1, selected_tasks))
        task_2 = next(filter(lambda t: t.tid == 2, selected_tasks))
        task_3 = next(filter(lambda t: t.tid == 3, task_1.childs))

        self.assertEquals(len(task_1.childs), 2)
        self.assertEquals(len(task_2.childs), 1)

        # 2 layout of depth test
        self.assertEquals(len(task_3.childs), 1)

        task_12 = next(filter(lambda t: t.tid == 12, selected_tasks))
        task_13 = next(filter(lambda t: t.tid == 13, selected_tasks))

        self.assertEquals(len(task_12.childs), 1)
        self.assertEquals(len(task_13.childs), 0)

        self._change_user(_USERS[2].uid)

        task_12 = next(filter(lambda t: t.tid == 12, selected_tasks))
        task_13 = next(filter(lambda t: t.tid == 13, selected_tasks))

        self.assertEquals(len(task_12.childs), 1)
        self.assertEquals(len(task_13.childs), 0)

    def test_union(self):
        fil_1 = TaskFilter().to_query()
        self.assertEqual(parse_string('').to_query(), fil_1)
