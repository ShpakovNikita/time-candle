from enums.priority import Priority
from enums.status import Status
from model import logger


class Task:
    """
    This is the base Task class for the task manager.
    """

    def __init__(self,
                 uid,
                 creator_uid,
                 tid,
                 # Replace later with the controller
                 deadline,
                 title,
                 pid=None,
                 status=Status.IN_PROGRESS,
                 priority=Priority.MEDIUM,
                 parent=None,
                 # instead of controller for now we have only deadline
                 # controller=None
                 comment='',
                 chat=None,
                 realization_time=-1):
        logger.debug('creating a task...')

        self.uid = uid
        self.creator_uid = creator_uid
        self.tid = tid
        self.pid = pid
        self.title = title
        self.status = status
        self.tags = []
        self.childs = []
        self.priority = priority
        self.parent = parent
        # self._controller = controller
        self.deadline = deadline
        self.comment = comment
        self.chat = chat
        self.realization_time = realization_time

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
