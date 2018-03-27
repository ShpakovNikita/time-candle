from src import adapters as a
from task import Task
from enums.priority import Priority
from helper_entities.controllers import BehaviorController
import  json

TASK_FILE = "task_"


def save(task, intend=4):
    if not isinstance(task, Task):
        raise ValueError("Passed argument should be an object of type Task, "
                         "passed argument is " + str(type(task)))

    file = a.check_for_database(a.DB_ROOT + "/" + a.TASKS_ROOT, TASK_FILE + "0")
    file.write("{\n")
    for key, value in task.__dict__.items():
        if isinstance(value, Priority):
            pass
        elif isinstance(value, BehaviorController):
            pass
        else:
            file.write(intend * " " + repr(key) + ":" + repr(value) + "\n")

    file.write("}")
