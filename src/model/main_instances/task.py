from enums.priority import Priority
from enums.status import Status
from model import logger


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
        logger.debug('creating a task...')

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

    @classmethod
    def make_task(cls, obj):
        """
        This function converts some data type to task
        :type obj: type with fields:
        - other obj receiver with uid
        - other obj creator with uid
        - tid
        - deadline_time
        - title
        - status
        - priority
        - other obj parent with tid or None
        - comment
        :return: Task
        """
        logger.debug('convert storage to model task')
        # we can have a None parent, so we have to determine this to take it's
        # id or not
        if obj.parent is None:
            parent_id = None
        else:
            parent_id = obj.parent.tid

        task = cls(obj.receiver.uid,
                   obj.creator.uid,
                   obj.tid,
                   obj.deadline_time,
                   obj.title,
                   None,
                   obj.status,
                   obj.priority,
                   parent_id,
                   obj.comment)

        return task
