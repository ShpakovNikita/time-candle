from time_candle.enums.priority import Priority
from time_candle.enums.status import Status
from time_candle.model import logger


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
                 realization_time=None,
                 creation_time=0,
                 period=None):
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
        self.period = period
        # self._controller = controller
        self.deadline = deadline
        self.comment = comment
        self.realization_time = realization_time
        self.creation_time = creation_time

    @classmethod
    def make_task(cls, obj):
        """
        This function converts some data type to task
        :type obj: type with fields:
        - receiver uid
        - creator uid
        - other obj project with pid
        - tid
        - deadline_time
        - title
        - status
        - priority
        - period
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

        if obj.project is None:
            project_id = None
        else:
            project_id = obj.project.pid

        task = cls(obj.receiver,
                   obj.creator,
                   obj.tid,
                   obj.deadline_time,
                   obj.title,
                   project_id,
                   obj.status,
                   obj.priority,
                   parent_id,
                   obj.comment,
                   obj.realization_time,
                   obj.creation_time,
                   obj.period)

        return task
