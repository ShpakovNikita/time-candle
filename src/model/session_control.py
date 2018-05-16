from model import config_parser
import storage.adapter_classes
import storage.task_adapter
import storage.user_adapter
import storage.project_adapter


def start_session():
    Adapters.TASK_ADAPTER = storage.task_adapter.\
        TaskAdapter()

    Adapters.PROJECT_ADAPTER = storage.project_adapter.\
        ProjectAdapter()

    Adapters.USER_ADAPTER = storage.user_adapter.\
        UserAdapter()

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
