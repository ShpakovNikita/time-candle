from django.shortcuts import redirect
from time_candle.enums.status import Status
from time_candle.model.time_formatter import get_datetime
from django.contrib.auth.models import User


def task_card_post_form(request, controller, redirect_link):
    if request.method == 'POST':
        if 'delete' in request.POST:
            controller.remove_task(request.POST['delete'])
            return redirect(redirect_link)

        elif 'check' in request.POST:
            controller.change_task(
                request.POST['check'], status=Status.DONE)
            return redirect(redirect_link)


def tasks_query_get_form(request, controller, default_query=''):
    if request.method == "GET":
        if 'show_me' in request.GET:
            if not default_query:
                query_form = request.GET['show_me']
            elif request.GET['show_me']:
                query_form = default_query + \
                             ' AND ( ' + request.GET['show_me'] + ' ) '
            else:
                query_form = default_query

            print(query_form)
            tasks_list = controller.get_tasks(query_form)

        else:
            tasks_list = controller.get_tasks(default_query)

        return tasks_list

    else:
        return []


def init_tasks(request, controller, tasks_list):
    for task in tasks_list:
        if task.deadline is not None:
            task.deadline = get_datetime(task.deadline)
        else:
            task.deadline = ''

        if task.realization_time is not None:
            task.realization_time = get_datetime(task.realization_time)
        else:
            task.realization_time = ''

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

        if task.parent:
            task.parent_task = controller.get_tasks('tids: ' + str(task.parent))[0]
