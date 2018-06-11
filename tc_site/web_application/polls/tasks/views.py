from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from .. import config
from . import shortcuts


def add_task(request):
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
                                parent_id=None,
                                comment=comment,
                                pid=None,
                                receiver_uid=None)

            return redirect('/polls/tasks')
    else:
        form = forms.AddTask()

    return render(request, 'polls/tasks/add_task.html', {'form': form})


def add_project_task(request, project_id):
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
                                parent_id=None,
                                comment=comment,
                                pid=None,
                                receiver_uid=None)

            return redirect(reverse('polls:tasks'))
    else:
        form = forms.AddTask()

    return render(request, reverse('polls:add_task'), {'form': form})


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
                                                      reverse('polls:project',
                                                              args=(project_id,)
                                                              ))
        if redirect_view:
            return redirect_view

        # convert all milliseconds fields to normal datetime
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value

    return render(request, 'polls/tasks/project.html', context)


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
                                                      reverse('polls:tasks'))
        if redirect_view:
            return redirect_view

        # convert all milliseconds fields to normal datetime.
        shortcuts.init_tasks(request, controller, tasks_list)

    except AppException as e:
        context['errors'] = e.errors.value

    return render(request, 'polls/tasks/tasks.html', context)
