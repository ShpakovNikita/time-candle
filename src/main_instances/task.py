from enums.priority import Priority
from enums.status import Status
from helper_entities import controllers
from datetime import datetime, date, time
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

    def __call__(self, *args, **kwargs):
        pass

    @classmethod
    def make_task(cls,
                  year=datetime.today().year,
                  # If this argument is None, then year will be ignored.
                  # Also it means that task will be created with current time as
                  # the deadline time.
                  time=None,
                  t_priority=Priority.MEDIUM):
        if time is None:
            controller = controllers.BehaviorController()
        elif isinstance(time, datetime):
            controller = controllers.BehaviorController(year=year,
                                                        month=time.month,
                                                        day=time.day,
                                                        hour=time.hour,
                                                        minute=time.minute)
        else:
            raise ValueError("Time must be an object of type datetime")

        return None

