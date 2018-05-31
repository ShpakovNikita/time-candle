import time_candle.storage.adapter_classes
import time_candle.storage.task_adapter
import time_candle.storage.user_adapter
import time_candle.storage.project_adapter
from time_candle.model import config_parser


"""This is the module for basic model logic. It uses storage adapters for some
logical validation and to send requests to the database.

"""


class Logic:

    def __init__(self, db_file=None):
        self.task_adapter = time_candle.storage.task_adapter. \
            TaskAdapter(db_file)

        self.project_adapter = time_candle.storage.project_adapter. \
            ProjectAdapter(db_file)

        self.user_adapter = time_candle.storage.user_adapter. \
            UserAdapter(db_file)

        self._login()

    def _login(self, user=None):
        """
        Returns loaded user to make some actions from it's name. User will be
        initialized from config file.
        :param user: User to login.
        :return: None
        """
        if user is not None:
            self.user = user
        else:
            self.user = config_parser.run_config()['user']

        self.user_adapter.uid = self.user.uid
        self.project_adapter.uid = self.user.uid
        self.task_adapter.uid = self.user.uid
