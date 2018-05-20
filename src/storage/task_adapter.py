from storage.adapter_classes import Task, User, UserProjectRelation, Project
from storage.adapter_classes import Filter as PrimaryFilter
from storage.adapter_classes import Adapter as PrimaryAdapter
from storage import logger
import exceptions.db_exceptions as db_e
from peewee import *


class TaskFilter(PrimaryFilter):
    OP_GREATER = 0
    OP_GREATER_OR_EQUALS = 1
    OP_EQUALS = 2
    OP_LESS_OR_EQUALS = 3
    OP_LESS = 4
    OP_NOT_EQUALS = 5

    def __init__(self):
        super().__init__()

    @staticmethod
    def _union_filter():
        return Task.tid.is_null(False)

    def tid(self, tid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        if isinstance(tid, (list,)):
            self.result.append(Task.tid << tid)
        else:
            self.result.append(Task.tid == tid)

        return self

    def creator(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        if isinstance(uid, (list,)):
            self.result.append(Task.creator << uid)
        else:
            self.result.append(Task.creator == uid)

        return self

    def receiver(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        if isinstance(uid, (list,)):
            self.result.append(Task.receiver << uid)
        else:
            self.result.append(Task.receiver == uid)

        return self

    def project(self, pid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        if isinstance(pid, (list,)):
            self.result.append(Task.project << pid)
        else:
            self.result.append(Task.project == pid)

        return self

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

        elif TaskFilter.OP_NOT_EQUALS == storage_op:
            self.result.append(Task.status != status)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

        return self

    def parent(self, tid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.parent == tid)
        return self

    def title_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.title.contains(substring))
        return self

    def title_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.title.contains(regex))
        return self

    def priority(self,
                 priority,
                 storage_op=OP_EQUALS,
                 op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.priority > priority)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            print(priority)
            self.result.append(Task.priority >= priority)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.priority == priority)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.priority <= priority)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.priority < priority)

        elif TaskFilter.OP_NOT_EQUALS == storage_op:
            self.result.append(Task.priority != priority)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

        return self

    def deadline_time(self,
                      deadline_time,
                      storage_op=OP_EQUALS,
                      op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.deadline_time > deadline_time)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.deadline_time >= deadline_time)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.deadline_time == deadline_time)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.deadline_time <= deadline_time)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.deadline_time < deadline_time)

        elif TaskFilter.OP_NOT_EQUALS == storage_op:
            self.result.append(Task.deadline_time != deadline_time)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

        return self

    def comment_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.comment.contains(substring))
        return self

    def comment_regex(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(Task.comment.contains(substring))
        return self

    def period(self,
               period,
               storage_op=OP_EQUALS,
               op=PrimaryFilter.OP_AND):
        # in this function we also have to compare on less or greater, that's
        # why another operator arg is needed
        if self.result:
            self.ops.append(op)

        if TaskFilter.OP_GREATER == storage_op:
            self.result.append(Task.period > period)

        elif TaskFilter.OP_GREATER_OR_EQUALS == storage_op:
            self.result.append(Task.period >= period)

        elif TaskFilter.OP_EQUALS == storage_op:
            self.result.append(Task.period == period)

        elif TaskFilter.OP_LESS_OR_EQUALS == storage_op:
            self.result.append(Task.period <= period)

        elif TaskFilter.OP_LESS == storage_op:
            self.result.append(Task.period < period)

        elif TaskFilter.OP_NOT_EQUALS == storage_op:
            self.result.append(Task.period != period)

        else:
            raise db_e.InvalidFilterOperator(db_e.FilterMessages.
                                             FILTER_DOES_NOT_EXISTS)

        return self


class TaskAdapter(PrimaryAdapter):
    def __init__(self, db_name=None, uid=None):
        super().__init__(uid, db_name)

    def get_by_filter(self, filter_instance):
        """
        This function returns storage objects by the given TaskFilter.
        :param filter_instance: TaskFilter with defined filters
        :return: List of Task objects
        """
        # in this query we get all available tasks (our personal tasks and all
        # tasks our in projects)
        query = self._get_available_tasks().select(). \
            join(User, on=((Task.creator == User.uid) |
                           (Task.receiver == User.uid))). \
            where(filter_instance.to_query()).group_by(Task)

        # return converted query to the outer module
        result = [task for task in query]
        return result

    def save(self, obj):
        """
        This function is used to store given task to the database. Note, that
        tasks can be with similar names and dates (but on that case I have a
        task below)
        :param obj: type with fields:
        - creator_uid
        - uid
        - pid
        - status
        - deadline_time
        - title
        - priority
        - parent with tid or None
        - comment
        :return: None
        """
        try:
            task = Task.select().where((Task.tid == obj.tid) &
                                       ((Task.receiver == self.uid) |
                                        (Task.creator == self.uid))).get()

            TaskAdapter._update(task, obj)

            logger.debug('task updated')
            return

        except DoesNotExist:
            logger.debug('adding task...')
        try:
            table_task = Task.create(creator=obj.creator_uid,
                                     receiver=obj.uid,
                                     project=obj.pid,
                                     status=obj.status,
                                     parent=obj.parent,
                                     title=obj.title,
                                     priority=obj.priority,
                                     deadline_time=obj.deadline,
                                     comment=obj.comment)
        except IntegrityError:
            # if you are guest
            raise db_e.InvalidLoginError(db_e.TaskMessages.DO_NOT_HAVE_RIGHTS)

        logger.debug('task\'s parent %s' % table_task.parent)

        logger.debug('task saved to database')

    def get_task_by_id(self, tid, pid=None):
        """
        This function finds task by id and current user in database and returns
        it, or raise error due to incorrect request
        :param pid: Project's id to get task from it
        :param tid: Task id to find
        :type pid: Int
        :type tid: Int
        :return: Task
        """
        # TODO: more flexible user dependency find for projects
        task = Task.select().where((Task.tid == tid) &
                                   ((Task.creator == self.uid) |
                                    (Task.receiver == self.uid)) &
                                   (Task.project == pid))
        try:
            return task.get()

        except DoesNotExist:
            logger.info('There is no such tid %s in the database for your user'
                        % tid)
            raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)

    def _get_available_tasks(self):
        # get all tasks in project related to user and his personal tasks
        query_projects = UserProjectRelation. \
            select().where(UserProjectRelation.user == self.uid)
        projects = [rel.project.pid for rel in query_projects]

        query = Task.select().where((Task.project << projects) |
                                    (Task.creator == self.uid))

        return query

    @staticmethod
    def _update(task, obj):
        task.creator = obj.creator_uid
        task.receiver = obj.uid
        task.project = obj.pid
        task.status = obj.status
        task.parent = obj.parent
        task.title = obj.title
        task.priority = obj.priority
        task.deadline_time = obj.deadline
        task.comment = obj.comment

        task.save()

    @staticmethod
    def last_id():
        """
        This function gets last id to add task on it's place
        TODO:
        This function finds the first unused id in the table to add new task row
        on that place
        :return: Int
        """
        query = Task.select().order_by(Task.tid.desc())
        logger.debug('getting last id from query...{}'
                     .format(query))

        try:
            # task query
            return query.get().tid

        except DoesNotExist:
            return 0

    def remove_task_by_id(self, tid):
        """
        This function removes selected task and it's all childs recursively or
        raises an exception if task does not exists
        :param tid: Tasks id
        :return: None
        """
        # TODO: Is that good to have a recursive try except?
        try:
            query = self._get_available_tasks().select().\
                where(Task.parent == tid)
            for task in query:
                self.remove_task_by_id(task.tid)

            logger.info('removing task by tid %s' % tid)
            task = self._get_available_tasks().\
                select().where(Task.tid == tid).get()

            task.delete_instance()

        except DoesNotExist:
            logger.info(
                'There is no such tid %s in the database for your user' % tid)
            raise db_e.InvalidTidError(db_e.TaskMessages.TASK_DOES_NOT_EXISTS)
