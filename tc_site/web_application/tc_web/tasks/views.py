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


def add_task(request, project_id=None, task_id=None):
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}
    controller = Controller(uid=request.user.id,
                            db_file=config.DATABASE_PATH)

    if request.method == 'POST':
        print(request.POST)
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
                try:
                    if 'search_receiver' in request.POST \
                            and request.POST['search_receiver']:
                        receiver_uid = User.objects.get(
                            username=request.POST['search_receiver']).id
                    else:
                        receiver_uid = None

                except User.DoesNotExist:
                    errors = type('dummy', (), {})()
                    errors.value = 'User does not exists in this project'
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
                if project_id is not None:
                    return redirect(
                        reverse('tc_web:project', args=(project_id,)))
                else:
                    return redirect(reverse('tc_web:tasks'))

            except AppException as e:
                context['errors'] = e.errors.value

    else:
        form = forms.AddTask()
        form.fields['title'].widget.attrs.update({'value': 'New Task'})
        form.fields['comment'].widget.attrs.update({'value': 'Nani!?'})

    context['form'] = form
    if project_id:
        try:
            context['project'] = controller.get_project(project_id)
        except AppException:
            raise Http404

    print(context)

    return render(request, 'tc_web/tasks/add_task.html', context)


def change_task(request, task_id):
    controller = Controller(uid=request.user.id,
                            db_file=config.DATABASE_PATH)

    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}

    if request.method == 'POST':
        print(request.POST)
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

            if not status:
                status = None
            else:
                status = int(status)

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

    else:
        form = forms.ChangeTask()

    context['form'] = form
    try:
        task = controller.get_tasks('tids: ' + str(task_id))[0]
        shortcuts.init_tasks(request, controller, [task])
        context['task'] = task
        form.fields['comment'].widget.attrs.update({'value': task.comment})
        form.fields['deadline_time'].widget.attrs.update({'value': task.deadline})

    except (AppException, IndexError):
        raise Http404

    return render(request, 'tc_web/tasks/change_task.html', context)


def project(request, project_id):
    if not request.user.is_authenticated:
        raise Http404

    for link in ['search', 'search_user']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    try:
        tasks_list = shortcuts.tasks_query_get_form(
            request, controller, 'projects: ' + str(project_id))
        shortcuts.sort_filter(request, tasks_list)

        users_list = controller.get_users(project_id)

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

        # convert all milliseconds fields to normal datetime
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value

    context['tasks_list'] = tasks_list
    context['users_list'] = users_list
    context['project'] = selected_project

    return render(request, 'tc_web/tasks/project.html', context)


def tasks(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    tasks_list = shortcuts.tasks_query_get_form(request, controller, '')
    shortcuts.sort_filter(request, tasks_list)

    try:
        redirect_view = shortcuts.task_card_post_form(request, controller,
                                                      reverse('tc_web:tasks'))
        if redirect_view:
            return redirect_view

        # convert all milliseconds fields to normal datetime.
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value
        shortcuts.init_tasks(request, controller, tasks_list)

    context['tasks_list'] = tasks_list

    return render(request, 'tc_web/tasks/tasks.html', context)
