from model import config_parser
import storage.adapter_classes
import storage.task_adapter
import storage.user_adapter
import storage.project_adapter
import sys
from exceptions import custom_excepthook


def start_session(dev_opt='dev', db_file=None):
    if dev_opt == 'dev':
        pass
    elif dev_opt == 'user':
        sys.excepthook = custom_excepthook
    else:
        raise ValueError('session option is wrong!')

    Adapters.TASK_ADAPTER = storage.task_adapter.\
        TaskAdapter(db_file)

    Adapters.PROJECT_ADAPTER = storage.project_adapter.\
        ProjectAdapter(db_file)

    Adapters.USER_ADAPTER = storage.user_adapter.\
        UserAdapter(db_file)

    Singleton.GLOBAL_USER = _login()

    Adapters.TASK_ADAPTER.uid = Singleton.GLOBAL_USER.uid
    Adapters.PROJECT_ADAPTER.uid = Singleton.GLOBAL_USER.uid
    Adapters.USER_ADAPTER.uid = Singleton.GLOBAL_USER.uid


class Singleton:
    GLOBAL_USER = None


class Adapters:
    USER_ADAPTER = None
    PROJECT_ADAPTER = None
    TASK_ADAPTER = None


def _login():
    """
    Returns loaded user to make some actions from it's name. User will be
    initialized from config file.
    :return: User
    """

    return config_parser.run_config()['user']
