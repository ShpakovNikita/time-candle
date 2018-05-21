from test_module import *
# TODO: later cleanup
from model.session_control import *
from model.commands import *
from model.tokenizer import *
# TODO: Mock. It is really hard to implement here. Like very-very-very hard.
# Assume that we tested or storage module very well


def _change_user(uid):
    Singleton.GLOBAL_USER = _USERS[uid - 1]
    Adapters.TASK_ADAPTER.uid = uid
    Adapters.USER_ADAPTER.uid = uid
    Adapters.PROJECT_ADAPTER.uid = uid


class TestTaskLogic(unittest.TestCase):

    def setUp(self):
        start_session(db_file=':memory:')
        _init_project_table()
        _init_user_table()

    def test_add_get_task(self):
        _change_user(_USERS[0].uid)

        # check that we can add tasks
        self.assertEqual(len(get_tasks('')), 0)
        add_task('asd', None, None, None, None, '', None, None)
        self.assertEqual(len(get_tasks('')), 1)

        # check that we do not have rights to see user's tasks
        _change_user(_USERS[1].uid)
        self.assertEqual(len(get_tasks('')), 0)


class TestTokenizer(unittest.TestCase):

    def test_union(self):
        fil_1 = TaskFilter().to_query()
        self.assertEqual(parse_string('').to_query(), fil_1)

    def test_cases(self):
        fil_1 = TaskFilter().receiver([1, 2, 3]).to_query()
        self.assertEqual(parse_string('receiver: 1 2 3').to_query(), fil_1)
