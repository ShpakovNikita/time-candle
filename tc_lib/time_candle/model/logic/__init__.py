"""
This is the module for basic model logic. It uses storage adapters for some
logical validation and to send requests to the database.
"""
import time_candle.storage.adapter_classes
import time_candle.storage.task_adapter
import time_candle.storage.project_adapter


class Logic:

    def __init__(self, db_file=None, uid=None):
        self.task_adapter = time_candle.storage.task_adapter. \
            TaskAdapter(db_file)

        self.project_adapter = time_candle.storage.project_adapter. \
            ProjectAdapter(db_file)

        self.user_adapter = time_candle.storage.user_adapter. \
            UserAdapter(db_file)

        self._auth(uid)

    def _auth(self, uid=None):
        """
        Returns loaded user to make some actions from it's name. User will be
        initialized from config file.
        :param user: User to login.
        :return: None
        """
        self.uid = uid

        self.project_adapter.uid = self.uid
        self.task_adapter.uid = self.uid
