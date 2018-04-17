from enums.priority import Priority
from helper_entities import controllers
from datetime import datetime, date, time as t
import json


class Task:
    """
    This is the base Task class for the task manager.
    """

    def __init__(self,
                 uid=-1,
                 creator_uid=-1,
                 tid=-1,
                 pid=-1,
                 t_status=None,
                 tags=[],
                 childs=[],
                 t_priority=Priority.MEDIUM,
                 parent=None,
                 controller=None,
                 comment='',
                 chat=None):
        self._uid = uid
        self._creator_uid = creator_uid
        self._tid = tid
        self._pid = pid
        self._status = t_status
        self._tags = tags
        self._childs = childs
        self._priority = t_priority
        self._parent = parent
        self._controller = controller
        self._comment = comment
        self._chat = chat

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

        return cls(controller=controller, t_priority=t_priority)

