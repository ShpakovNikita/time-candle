from enums.priority import Priority
from enums.status import Status
import app_logger


class Task:
    """
    This is the base Task class for the task manager.
    """

    def __init__(self,
                 uid_,
                 creator_uid_,
                 tid_,
                 # Replace later with the controller
                 deadline_,
                 title_,
                 pid_=None,
                 status_=Status.IN_PROGRESS,
                 priority_=Priority.MEDIUM,
                 parent_=None,
                 # instead of controller for now we have only deadline
                 # controller=None
                 comment_='',
                 chat_=None):
        app_logger.custom_logger('model').debug('creating a task...')

        self.uid = uid_
        self.creator_uid = creator_uid_
        self.tid = tid_
        self.pid = pid_
        self.title = title_
        self.status = status_
        self.tags = []
        self.childs = []
        self.priority = priority_
        self.parent = parent_
        # self._controller = controller
        self.deadline = deadline_
        self.comment = comment_
        self.chat = chat_
