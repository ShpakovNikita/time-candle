"""
This is the module for basic model logic. It uses storage adapters for some
logical validation and to send requests to the database.
"""
import time_candle.storage.adapter_classes
import time_candle.storage.task_adapter
import time_candle.storage.project_adapter
import time_candle.storage.user_adapter


class MessagesQueue:

    def __init__(self, message_adapter):
        """
        Constructor
        :param message_adapter: of course it is UserAdapter, but in this case we
         will only use message methods
        """
        self.queue = []
        self.message_adapter = message_adapter

    def append(self, receiver, message_content):
        """
        Appends message instance to the queue
        :param message_content: message string
        :param receiver: receiver's id
        :return: None
        """
        self.queue.append((message_content, receiver))

    def flush(self):
        """
        Use this function to send all messages previously added to the object
        :return: None
        """
        for message_content, receiver in self.queue:
            self.message_adapter.send_message(receiver, message_content)

        self.queue.clear()


class Logic:

    def __init__(self,
                 db_file=None,
                 uid=None,
                 psql_config=None,
                 connect_url=None):
        self.task_adapter = time_candle.storage.task_adapter. \
            TaskAdapter(db_name=db_file, psql_config=psql_config,
                        connect_url=connect_url)

        self.project_adapter = time_candle.storage.project_adapter. \
            ProjectAdapter(db_name=db_file, psql_config=psql_config,
                           connect_url=connect_url)

        self.user_adapter = time_candle.storage.user_adapter. \
            UserAdapter(db_name=db_file, psql_config=psql_config,
                        connect_url=connect_url)

        self._auth(uid)
        self.queue = MessagesQueue(self.user_adapter)

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
        self.user_adapter.uid = self.uid
