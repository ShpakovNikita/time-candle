from django.http import Http404
from django.shortcuts import (
    render,
    redirect,
)
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from tc_web.tasks import forms
from tc_web import config
from tc_web.tasks import shortcuts
from tc_web import shortcuts as base
from django.contrib.auth.models import User
from tc_web import logger


def add_task(request, project_id=None, task_id=None):
    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}
    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    if request.method == 'POST':
        form = forms.AddTask(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            comment = form.cleaned_data.get('comment')
            deadline_time = form.cleaned_data.get('deadline_time')
            priority = form.cleaned_data.get('priority')
            status = form.cleaned_data.get('status')
            period = form.cleaned_data.get('period')
            if not deadline_time:
                deadline_time = None

            try:

                # this try is needed inside other try in order to skip adding
                # task id we haven't found our user
                try:
                    if 'search_receiver' in request.POST \
                            and request.POST['search_receiver']:
                        receiver_uid = User.objects.get(
                            username=request.POST['search_receiver']).id
                    else:
                        receiver_uid = None

                except User.DoesNotExist:
                    # this done for more elegant way to catch exception
                    errors = type('dummy', (), {})()
                    errors.value = 'User does not exists in this project'
                    logger.warning(errors.value)
                    raise AppException(errors)

                controller.add_task(title=title,
                                    time=deadline_time,
                                    priority=int(priority),
                                    status=int(status),
                                    period=period,
                                    parent_id=task_id,
                                    comment=comment,
                                    pid=project_id,
                                    receiver_uid=receiver_uid)
                # for better user experience we are checking where to go: to the
                # project if task is project's or to the tasks page
                if project_id is not None:
                    return redirect(
                        reverse('tc_web:project', args=(project_id,)))
                else:
                    return redirect(reverse('tc_web:tasks'))

            except AppException as e:
                context['errors'] = e.errors.value
                logger.warning(e.errors.value)

    else:
        form = forms.AddTask()

        # init form fields with default values
        form.fields['title'].widget.attrs.update({'value': 'New Task'})
        form.fields['comment'].widget.attrs.update({'value': 'Nani!?'})

    context['form'] = form

    # check if we have rights to be on this page
    if project_id:
        try:
            context['project'] = controller.get_project(project_id)
        except AppException:
            raise Http404

    return render(request, 'tc_web/tasks/add_task.html', context)


def change_task(request, task_id):
    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}
    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    if request.method == 'POST':
        form = forms.ChangeTask(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            deadline_time = form.cleaned_data.get('deadline_time')
            priority = form.cleaned_data.get('priority')
            status = form.cleaned_data.get('status')

            if not deadline_time:
                deadline_time = None

            if not comment:
                comment = None

            # convert to int if field checked
            if not status:
                status = None
            else:
                status = int(status)

            # convert to int if field checked
            if not priority:
                priority = None
            else:
                priority = int(priority)

            try:
                controller.change_task(tid=task_id,
                                       priority=priority,
                                       status=status,
                                       time=deadline_time,
                                       comment=comment)
                return redirect(reverse('tc_web:tasks'))

            except AppException as e:
                context['errors'] = e.errors.value
                logger.warning(e.errors.value)

    else:
        form = forms.ChangeTask()

    context['form'] = form

    # check if we can see this page
    try:
        task = controller.get_tasks('tids: ' + str(task_id))[0]
        shortcuts.init_tasks(request, controller, [task])
        context['task'] = task
        form.fields['comment'].widget.attrs.update({'value': task.comment})
        form.fields['deadline_time'].widget.attrs.update({'value': task.deadline})

    except (AppException, IndexError):
        logger.warning('error occured during the change task')
        raise Http404

    return render(request, 'tc_web/tasks/change_task.html', context)


def project(request, project_id):
    if not request.user.is_authenticated:
        logger.warning('user is not authenticated')
        raise Http404

    # we always init our search form
    for link in ['search', 'search_user']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}
    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    try:
        # loading selected tasks
        tasks_list = shortcuts.tasks_query_get_form(
            request, controller, 'projects: ' + str(project_id))
        shortcuts.sort_filter(request, tasks_list)
    except AppException as e:
        context['errors'] = e.errors.value
        tasks_list = controller.get_tasks('projects: ' + str(project_id))
        shortcuts.sort_filter(request, tasks_list)

    try:
        # get users for side nav
        users_list = controller.get_users(project_id)

        # and the project itself for more information on the page
        selected_project = controller.get_project(project_id)
        selected_project.admin = User.objects.get(id=selected_project.admin_uid)

    except AppException:
        raise Http404

    try:
        redirect_view = shortcuts.task_card_post_form(request,
                                                      controller,
                                                      reverse('tc_web:project',
                                                              args=(project_id,)
                                                              ))
        if redirect_view:
            return redirect_view

        # convert and add fields
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value
        logger.warning(e.errors.value)

        # error won't stop us from showing the tasks!
        shortcuts.init_tasks(request, controller, tasks_list)

    context['tasks_list'] = tasks_list
    context['users_list'] = users_list
    context['project'] = selected_project

    return render(request, 'tc_web/tasks/project.html', context)


def tasks(request):
    if not request.user.is_authenticated:
        logger.warning('user is not authenticated')
        return redirect('/login/')

    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}

    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    # loading selected tasks
    try:
        tasks_list = shortcuts.tasks_query_get_form(request, controller, '')
    except AppException as e:
        context['errors'] = e.errors.value
        tasks_list = controller.get_tasks()
        shortcuts.sort_filter(request, tasks_list)

    shortcuts.sort_filter(request, tasks_list)

    try:
        redirect_view = shortcuts.task_card_post_form(request, controller,
                                                      reverse('tc_web:tasks'))
        if redirect_view:
            return redirect_view

        # convert and add fields
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value
        logger.warning(e.errors.value)

        # error won't stop us from showing the tasks!
        shortcuts.init_tasks(request, controller, tasks_list)

    context['tasks_list'] = tasks_list

    return render(request, 'tc_web/tasks/tasks.html', context)
