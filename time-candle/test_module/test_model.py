from test_module import *
# TODO: later cleanup
from model.session_control import *
from model.commands import *
from model.tokenizer import *
import exceptions.show_me_exceptions as sm_e


# TODO: Mock. It is really hard to implement here. Like very-very-very hard.
# Assume that we tested or storage module very well


def _change_user(uid):
    Singleton.GLOBAL_USER = _USERS[uid - 1]
    Adapters.TASK_ADAPTER.uid = uid
    Adapters.USER_ADAPTER.uid = uid
    Adapters.PROJECT_ADAPTER.uid = uid


class TestTaskLogic(unittest.TestCase):
    # Note that we also testing our tokenizer

    def setUp(self):
        start_session(db_file=':memory:')
        _init_project_table()
        _init_user_table()

    def tearDown(self):
        User.delete().execute()
        Task.delete().execute()
        Project.delete().execute()
        UserProjectRelation.delete().execute()

    def test_simple_add_get_task(self):
        _change_user(_USERS[0].uid)
        # check that we can add tasks
        self.assertEqual(len(get_tasks('')), 0)
        add_task('asd', None, None, None, None, '', None, None)
        self.assertEqual(len(get_tasks('')), 1)

        # check that we do not have rights to see user's tasks
        _change_user(_USERS[1].uid)
        self.assertEqual(len(get_tasks('')), 0)

        # remove not ours task
        _change_user(_USERS[0].uid)
        remove_task(1)
        self.assertEqual(len(get_tasks('')), 0)

    def test_get_by_filter(self):
        _init_task_table()
        _init_project_tasks_table()

        _change_user(_USERS[0].uid)
        # let's test our filter tokenizer
        self.assertEqual(len(get_tasks('')), 19)
        self.assertEqual(len(get_tasks('projects: None')), 7)
        self.assertEqual(len(get_tasks('projects: None AND titles: tesg 3')), 3)
        self.assertEqual(len(get_tasks('projects: None AND titles: tesg 4')), 2)

        self.assertEqual(
            len(get_tasks('(projects: None AND titles: tesg 3) OR tids: 9 10')),
            5)
        self.assertEqual(
            len(get_tasks('(projects:  None AND titles: tesg 3) OR tids: 9 4')),
            4)
        self.assertEqual(
            len(get_tasks('(projects: None OR projects: 1) AND titles: pr')), 4)
        self.assertEqual(
            len(get_tasks('(projects: None OR projects: 1) AND (titles: pr)')),
            4)
        self.assertEqual(
            len(get_tasks(
                '(projects: None OR projects: 1) AND (titles: pr OR tids: 1 2)')
                ), 6)

        # relog test
        _change_user(_USERS[1].uid)
        self.assertNotEqual(
            len(get_tasks('(projects: None AND titles: tesg 3) OR tids: 9 10')),
            5)

        # check it on the error situations
        with self.assertRaises(sm_e.InvalidExpressionError):
            get_tasks('dsa')

        with self.assertRaises(sm_e.InvalidExpressionError):
            get_tasks('projects: dsa 2 3')

        with self.assertRaises(sm_e.InvalidExpressionError):
            get_tasks('projects: 1 2 3 AND OR projects: 2 3')

        with self.assertRaises(sm_e.InvalidExpressionError):
            get_tasks('projects: 1 2 3 AND ()')

    def test_add_validations(self):
        pass

    def test_union(self):
        fil_1 = TaskFilter().to_query()
        self.assertEqual(parse_string('').to_query(), fil_1)
