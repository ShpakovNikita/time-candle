from time_candle.model.instances.task import Task as TaskInstance
import time_candle.exceptions.model_exceptions as m_e
from time_candle.model import logger
import time_candle.model.tokenizer
import time_candle.model.time_formatter
from time_candle.enums.status import Status
from . import Logic


class TaskLogic(Logic):

    def __init__(self,
                 db_name=None,
                 uid=None,
                 psql_config=None,
                 connect_url=None):
        super().__init__(db_name, uid, psql_config, connect_url)

    def add_task(self, title, priority, status, deadline_time,
                 parent_id, comment, pid, uid, period):
        # add task to the database

        # This code is also checking is our parent tid exists in the database
        # for logged user. The max func needed to set tasks status and priority
        # not lower then parent's
        if parent_id is not None:
            parent_task = self.task_adapter.get_task_by_id(parent_id)
            status = max(status, parent_task.status)
            priority = max(priority, parent_task.priority)

        logger.debug('time in milliseconds %s', deadline_time)
        logger.info('time now (from milliseconds to datetime) %s',
                    time_candle.model.time_formatter.get_datetime(
                        time_candle.model.time_formatter.get_now_milliseconds()
                    ))

        # Check for rights and id's
        if uid is None:
            task_uid = self.uid
        else:
            self.project_adapter.is_user_in_project(uid, pid)
            task_uid = uid

        # check that if we are in the project that we has proper rights
        if pid is not None:
            logger.debug('pid is not none')
            if task_uid != self.uid:
                logger.debug('the receiver is not us')
                if self.project_adapter.has_rights(pid):
                    raise m_e.InvalidLoginError(
                        m_e.ProjectMessages.DO_NOT_HAVE_RIGHTS)
            else:
                logger.debug('we are the receiver')
                self.project_adapter.is_user_in_project(self.uid, pid)

        # if deadline is not none
        if deadline_time is not None:
            # we checking that deadline is in the future
            if time_candle.model.time_formatter.time_delta(deadline_time) < 0:
                raise m_e.InvalidTimeError(m_e.TimeMessages.TIME_SHIFT)

        # also we must specify deadline if there is a period
        if period is not None and deadline_time is None:
            raise m_e.InvalidTimeError(m_e.TimeMessages.NO_DEADLINE)

        if period is not None and period < 0:
            raise m_e.InvalidTimeError(m_e.TimeMessages.NEGATIVE_PERIOD)

        if status == Status.EXPIRED and deadline_time is None:
            raise m_e.InvalidTimeError(m_e.TimeMessages.NO_DEADLINE)

        if status == Status.DONE:
            realization_time = time_candle.model.time_formatter.\
                get_now_milliseconds()
        else:
            realization_time = None

        task = TaskInstance(uid=task_uid,
                            creator_uid=self.uid,
                            tid=self.task_adapter.last_id() + 1,
                            deadline=deadline_time,
                            title=title,
                            pid=pid,
                            status=status,
                            priority=priority,
                            parent=parent_id,
                            comment=comment,
                            realization_time=realization_time,
                            creation_time=time_candle.model.time_formatter.
                            get_now_milliseconds(),
                            period=period)

        logger.debug('task configured and ready to save , the task id is %s',
                     task.tid)

        self.task_adapter.save(task)

        logger.debug('task added')

    def has_rights_to_modify(self, tid):
        return self.task_adapter.has_rights(tid)

    def remove_task(self, tid):
        # remove task from database
        self.task_adapter.remove_task_by_id(tid)

    def change_task(self, tid, priority, status, time, comment):
        # change task in the database
        task = self.task_adapter.get_task_by_id(tid)
        if task.parent is not None:
            parent_task = self.task_adapter.get_task_by_id(task.parent)
            if status is not None:
                status = max(status, parent_task.status)

            if priority is not None:
                priority = max(priority, parent_task.priority)

        if priority is not None:
            task.priority = priority
        if status is not None:
            # if status is not done, then realization time is None
            if status != Status.DONE:
                task.realization_time = None

            if status == Status.EXPIRED and time is None:
                raise m_e.InvalidTimeError(m_e.TimeMessages.NO_DEADLINE)

            # we cannot change done task to the expired. Note, that we can make
            # done task as some other task and then we may change it to expired
            elif status == Status.EXPIRED and task.status == Status.DONE:
                raise m_e.InvalidStatusError(
                    m_e.StatusMessages.EXPIRED_NOT_VALID)

            task.status = status
            # mark time for the done task
            if status == Status.DONE:
                task.realization_time = time_candle.model.time_formatter.\
                    get_now_milliseconds()

        if time is not None:
            # if the time is like before, it can be in the past. But in any
            # other cases it is not logical to move deadlines in the past
            if task.deadline != time:
                # we cannot allow to make deadline in the past
                if time_candle.model.time_formatter.time_delta(time) < 0:
                    raise m_e.InvalidTimeError(m_e.TimeMessages.TIME_SHIFT)

                # also we should make task unexpired if we moved deadline and it
                # was expired
                if task.status == Status.EXPIRED:
                    task.status = Status.IN_PROGRESS

            task.deadline = time

        if comment is not None:
            task.comment = comment

        self.task_adapter.save(task)

    def get_tasks(self, string_fil):
        # get tasks by filter
        fil = time_candle.model.tokenizer.parse_string(string_fil)
        tasks = self.task_adapter.get_by_filter(fil)
        for task in tasks:
            self._update(task)

        return tasks

    def _update(self, task):
        changed_flag = False
        # make tasks expired if deadline is crossed
        if task.deadline is not None \
                and time_candle.model.\
                time_formatter.time_delta(task.deadline) < 0 \
                and task.status == Status.IN_PROGRESS:
            task.status = Status.EXPIRED
            logger.debug('tasks status updated')
            changed_flag = True

        # make new deadline to the period task if there is need to do so and if
        # we are not expired our task
        if task.period is not None:
            old_deadline = task.deadline
            # check on expired and maybe change deadline
            if task.status != Status.EXPIRED:
                task.deadline = time_candle.model.time_formatter.\
                    get_next_deadline(task.period, task.deadline)

            # if we are changed it then we are in progress
            if old_deadline != task.deadline:
                task.status = Status.IN_PROGRESS
                logger.debug('status in progress for period task %s', task.tid)
                changed_flag = True

        if changed_flag:
            self.task_adapter.save(task)
            logger.debug('task updated')
