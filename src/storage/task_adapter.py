from storage.adapter_classes import Task, User
from storage.adapter_classes import Filter as PrimaryFilter
from storage import logger
from main_instances.task import Task as TaskInstance
import exceptions.db_exceptions as db_e
from singleton import Singleton
from peewee import *


class TaskFilter(PrimaryFilter):
    OP_GREATER = 0
    OP_GREATER_OR_EQUALS = 1
    OP_EQUALS = 2
    OP_LESS_OR_EQUALS = 3
    OP_LESS = 4

    def __init__(self):
        super().__init__()

    def tid(self, tid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.id == tid)

    def creator(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.creator == uid)

    def receiver(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.receiver == uid)

    def project(self, pid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.project == pid)

    def status(self,
               status,
               storage_op=OP_EQUALS,
               op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.status > status)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.status >= status)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.status == status)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.status <= status)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.status < status)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

    def parent(self, tid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.parent == tid)

    def title_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.title.contains(substring))

    def title_regex(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.title.contains(substring))

    def priority(self,
                 priority,
                 storage_op=OP_EQUALS,
                 op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.status > priority)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.status >= priority)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.status == priority)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.status <= priority)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.status < priority)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

    def deadline_time(self,
                      deadline_time,
                      storage_op=OP_EQUALS,
                      op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.status > deadline_time)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.status >= deadline_time)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.status == deadline_time)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.status <= deadline_time)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.status < deadline_time)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

    def comment_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.comment.contains(substring))

    def comment_regex(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.comment.contains(substring))

    def period(self,
               period,
               storage_op=OP_EQUALS,
               op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.status > period)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.status >= period)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.status == period)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.status <= period)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.status < period)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)


def save(task):
    """
    This function is used to store given task to the database. Note, that tasks
    can be with similar names and dates (but on that case I have a task below)
    TODO: warning if the task's title and time are matching with some precision
    :param task: This is our task to save
    :type task: TaskInstance
    :return: None
    """
    try:
        Task.select().where(Task.id == task.tid).get()
        update()
        logger.debug('task updated')

    except DoesNotExist:
        logger.debug('adding task...')

    table_task = Task.create(creator=task.creator_uid,
                             receiver=task.uid,
                             project=task.pid,
                             status=task.status,
                             parent=task.parent,
                             title=task.title,
                             priority=task.priority,
                             deadline_time=task.deadline,
                             comment=task.comment)

    logger.debug('taks\'s parent %s' % table_task.parent)

    logger.debug('task saved to database')


def last_id():
    """
    This function gets last id to add task on it's place
    TODO:
    This function finds the first unused id in the table to add new task row on
    that place
    :return: Int
    """

    query = Task.select().order_by(Task.id.desc())
    logger.debug('getting last id from query...{}'
                                              .format(query))

    try:
        return query.get().id

    except DoesNotExist:
        return 1


def remove_task_by_id(tid):
    """
    This function removes selected task and it's all childs recursively or
    raises an exception if task does not exists
    :param tid: Tasks id
    :return: None
    """
    # TODO: Is that good to have a recursive try except?
    try:
        query = Task.select().where(Task.parent == tid)
        for task in query:
            remove_task_by_id(task.id)

        logger.info('removing task by tid %s' % tid)
        Task.delete().where(Task.id == tid).execute()
    except DoesNotExist:
        logger.info('There is no such tid %s in the database for your user' %
                    tid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def get_task_by_id(tid, pid=None):
    """
    This function finds task by id and current user in database and returns it,
    or raise error due to incorrect request
    :param pid: Project's id to get task from it
    :param tid: Task id to find
    :type pid: Int
    :type tid: Int
    :return: Task
    """
    # TODO: more flexible user dependency find for projects
    task = Task.select().where((Task.id == tid) &
                               ((Task.creator == Singleton.GLOBAL_USER.uid) |
                                (Task.receiver == Singleton.GLOBAL_USER.uid)) &
                               (Task.project == pid))
    try:
        return _storage_to_model(task.get())

    except DoesNotExist:
        logger.info('There is no such tid %s in the database for your user' %
                    tid)
        raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)


def update():
    pass


def _storage_to_model(storage_task):
    """
    This function converts storage task to model task
    :type storage_task: Task
    :return: TaskInstance
    """
    logger.debug('convert storage to model task')
    # we can have a None parent, so we have to determine this to take it's id or
    # not
    if storage_task.parent is None:
        parent_id = None
    else:
        parent_id = storage_task.parent.id

    model_task = TaskInstance(storage_task.receiver.id,
                              storage_task.creator.id,
                              storage_task.id,
                              storage_task.deadline_time,
                              storage_task.title,
                              None,
                              storage_task.status,
                              storage_task.priority,
                              parent_id,
                              storage_task.comment)

    return model_task
