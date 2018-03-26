from src.enums import priority
from src.helper_entities import controllers


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
                 t_priority=None,
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
                  time=None,
                  t_priority=priority.Priority.MEDIUM):
        if time is None:
            controller = controllers.BehaviorController()
        else:
            controller = controllers.BehaviorController()

        return cls(controller=controller, t_priority=t_priority)


def main():
    file = open('data.json', 'w+')
    pass


if __name__ == "__main__":
    main()
