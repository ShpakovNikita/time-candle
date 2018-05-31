from test_module import *
from time_candle.controller.commands import Controller
from time_candle.model.tokenizer import parse_string
import time_candle.exceptions.show_me_exceptions as sm_e


# TODO: Mock. It is really hard to implement here. Like very-very-very hard.
# Assume that we tested or storage module very well


class TestTaskLogic(unittest.TestCase):
    # Note that we also testing our tokenizer

    def _change_user(self, uid):
        self.controller.task_logic._login(_USERS[uid - 1])
        self.controller.user_logic._login(_USERS[uid - 1])
        self.controller.project_logic._login(_USERS[uid - 1])

    def setUp(self):
        self.controller = Controller(mode='dev', db_file=db_file)

        _init_project_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
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

    def test_get_by_filter(self):
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

    def test_union(self):
        fil_1 = TaskFilter().to_query()
        self.assertEqual(parse_string('').to_query(), fil_1)
