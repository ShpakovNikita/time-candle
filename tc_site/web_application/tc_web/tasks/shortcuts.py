from django.shortcuts import redirect
from time_candle.enums.status import Status
from time_candle.enums.priority import Priority
from time_candle.model.time_formatter import (
    get_datetime,
    milliseconds_to_days,
)
from tc_web import logger


# use it do define all post forms related to tasks
def task_card_post_form(request, controller):
    logger.debug('post_check')
    if request.method == 'POST':
        logger.debug(request.POST)
        if 'delete' in request.POST:
            print(request.POST['delete'])
            controller.remove_task(request.POST['delete'])
            print('success')
            return redirect(request.META.get('HTTP_REFERER'))

        elif 'check' in request.POST:
            controller.change_task(
                request.POST['check'], status=Status.DONE)
            return redirect(request.META.get('HTTP_REFERER'))


# use this to get tasks. It checks if there was applied query and returns proper
# tasks with filter
def tasks_query_get_form(request, controller, default_query=''):
    if request.method == "GET":
        logger.debug(request.GET)
        if 'show_me' in request.GET:
            if not default_query:
                query_form = request.GET['show_me']
            elif request.GET['show_me']:
                query_form = default_query + \
                             ' AND ( ' + request.GET['show_me'] + ' ) '
            else:
                query_form = default_query

            tasks_list = controller.get_tasks(query_form)

        else:
            tasks_list = controller.get_tasks(default_query)

    else:
        tasks_list = controller.get_tasks(default_query)

    return tasks_list


# use this function as sort. It makes your user goes first and by priority,
# other tasks that is not yours goes later by priority
def sort_filter(request, tasks_list):
    def custom_filter(task):
        if task.uid == request.user.id:
            return task.priority

        else:
            return task.priority - Priority.MAX

    tasks_list.sort(key=custom_filter, reverse=True)


# use this function to initialize some additional fields to the library model
# for better view and user experience or convert existing values
def init_tasks(request, controller, tasks_list):
    for task in tasks_list:

        # convert from milliseconds to datetime
        if task.deadline is not None:
            task.deadline = get_datetime(task.deadline)
        else:
            task.deadline = ''

        # convert from milliseconds to datetime
        if task.realization_time is not None:
            task.realization_time = get_datetime(task.realization_time)
        else:
            task.realization_time = ''

        if task.period is not None:
            task.period = milliseconds_to_days(task.period)

        # this value is always defined
        task.creation_time = get_datetime(task.creation_time)

        if task.pid is not None:
            task.project_name = controller.get_project(task.pid).title

            # this is what we need to know if user was inited (just to skip
            # twice db call)
            user = None
            if task.uid == request.user.id:
                task.receiver_name = 'You'
            else:
                user = controller.get_user(task.uid)
                task.receiver_name = user.login

            if task.creator_uid == request.user.id:
                task.creator_name = 'You'
            else:
                if not user:
                    task.creator_name = controller.get_user(
                        task.creator_uid).login
                else:
                    task.creator_name = user.login

            task.has_rights = controller.has_rights_to_modify_task(task.tid)

        else:
            task.has_rights = True

        if task.parent:
            task.parent_task = controller.get_tasks('tids: ' + str(task.parent))[0]
