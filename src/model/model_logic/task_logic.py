from model.model_logic import *


def add_task(title, priority, status, time, parent_id, comment, pid, login):
    # add task to the database

    # This max func needed to set tasks status and priority not lower then
    # parent's
    if priority is None:
        logger.debug('Default priority has been set')
        priority = Priority.MEDIUM

    if status is None:
        logger.debug('Default status has been set')
        status = Status.IN_PROGRESS

    # This code is also checking is our parent tid exists in the database for
    # logged user. The max func needed to set tasks status and priority not
    # lower then parent's

    # TODO: parent pid match pid
    if parent_id is not None:
        parent_task = TaskInstance.make_task(
            Adapters.TASK_ADAPTER.get_task_by_id(parent_id, pid))
        status = max(status, parent_task.status)
        priority = max(priority, parent_task.priority)

    deadline_time = None

    if time is not None:
        deadline_time = validators.get_milliseconds(time)

    logger.debug('time in milliseconds %s' % deadline_time)

    # TODO: MADE NOT ONLY ADMIN ADD, BUT USERS WITH LOW PRIORITY!!! Just change
    # TODO: on is_admin(pid) maybe

    # Check for rights and id's
    if login is None:
        task_uid = Singleton.GLOBAL_USER.uid
    else:
        Adapters.USER_ADAPTER.is_user_in_project(login, pid)
        task_uid = Adapters.USER_ADAPTER.get_id_by_login(login)

    if pid is not None:
        Adapters.PROJECT_ADAPTER.has_rights(pid)

    task = TaskInstance(task_uid,
                        Singleton.GLOBAL_USER.uid,
                        Adapters.TASK_ADAPTER.last_id() + 1,
                        deadline_time,
                        title,
                        pid,
                        status,
                        priority,
                        parent_id,
                        comment)

    logger.debug('task configured and ready to save , the task id is %s'
                 % task.tid)

    Adapters.TASK_ADAPTER.save(task)

    logger.debug('task added')


def remove_task(tid):
    # remove task from database
    Adapters.TASK_ADAPTER.remove_task_by_id(tid)


def change_task(tid, priority, status, time, comment):
    # change task in the database
    task = TaskInstance.make_task(Adapters.TASK_ADAPTER.get_task_by_id(tid))
    if priority is not None:
        task.priority = priority
    if status is not None:
        task.status = status
    if time is not None:
        task.deadline = time
    if comment is not None:
        task.comment = comment

    Adapters.TASK_ADAPTER.save(task)
