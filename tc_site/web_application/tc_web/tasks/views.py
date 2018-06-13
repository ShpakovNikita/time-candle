from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from .. import config
from . import shortcuts


def add_task(request, project_id=None, task_id=None):
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

            controller = Controller(uid=request.user.id,
                                    db_file=config.DATABASE_PATH)

            controller.add_task(title=title,
                                time=deadline_time,
                                priority=int(priority),
                                status=int(status),
                                period=period,
                                parent_id=task_id,
                                comment=comment,
                                pid=project_id,
                                receiver_uid=None)
            if project_id is not None:
                return redirect(reverse('tc_web:project', args=(project_id,)))
            else:
                return redirect(reverse('tc_web:tasks'))
    else:
        form = forms.AddTask()
        form.fields['title'].widget.attrs.update({'value': 'New Task'})

    return render(request, 'tc_web/tasks/add_task.html', {'form': form})


def change_task(request, task_id):
    controller = Controller(uid=request.user.id,
                            db_file=config.DATABASE_PATH)

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

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    tasks_list = controller.get_tasks('projects: ' + str(project_id))
    context = {
        'tasks_list': tasks_list
    }

    try:
        selected_project = controller.get_project(project_id)
        context['project'] = selected_project

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

    return render(request, 'tc_web/tasks/project.html', context)


def tasks(request):
    if not request.user.is_authenticated:
        raise Http404

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    tasks_list = controller.get_tasks('')[:5]
    context = {
        'tasks_list': tasks_list
    }

    try:
        redirect_view = shortcuts.task_card_post_form(request, controller,
                                                      reverse('tc_web:tasks'))
        if redirect_view:
            return redirect_view

        # convert all milliseconds fields to normal datetime.
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value

    return render(request, 'tc_web/tasks/tasks.html', context)
