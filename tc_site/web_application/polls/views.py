from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from time_candle.model.time_formatter import get_datetime
from .models import Question, Choice, DoesNotExist
from time_candle.enums.status import Status
from . import config


def err404(request, exception):
    return render(
        request, 'polls/404.html', status=404)


def index(request):
    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)
    latest_question_list = controller.get_tasks('')[:5]
    template = loader.get_template('polls/index.html')
    controller.get_tasks('tids: 10')

    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    template = loader.get_template('polls/detail.html')
    try:
        question = Question.get(Question.id == question_id)
    except DoesNotExist:
        raise Http404

    context = {'question': question}
    return HttpResponse(template.render(context, request))


def results(request, question_id):
    try:
        question = Question.get(Question.id == question_id)
    except DoesNotExist:
        raise Http404

    return render(request, 'polls/results.html', {'question': question})


def tasks(request):
    if not request.user.is_authenticated:
        raise Http404

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)
    if request.method == 'POST':
        if 'delete' in request.POST:
            try:
                controller.remove_task(request.POST['delete'])
                return redirect('/polls/tasks')
            except AppException:
                pass

        elif 'check' in request.POST:
            try:
                controller.change_task(
                    request.POST['check'], status=Status.DONE)
                return redirect('/polls/tasks')
            except AppException as e:
                print(e.errors)

    tasks_list = controller.get_tasks('')[:5]

    # convert all milliseconds fields to normal datetime
    for task in tasks_list:
        task.pid = 1
        if task.deadline is not None:
            task.deadline = get_datetime(task.deadline)
        else:
            task.deadline = None

        if task.pid is not None:
            task.project_name = controller.get_project(task.pid).title
            if task.uid == request.user.id:
                task.receiver_name = 'You'
            else:
                task.receiver_name = controller.get_user(task.uid).login

    context = {
        'tasks_list': tasks_list
    }

    return render(request, 'polls/tasks.html', context)


def projects(request):
    if not request.user.is_authenticated:
        raise Http404
    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)
    projects_list = controller.get_projects('')[:5]

    context = {
        'projects_list': projects_list
    }

    return render(request, 'polls/projects.html', context)


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

    return render(request, 'polls/add_task.html', {'form': form})


def add_project(request):
    if request.method == 'POST':
        print(request.POST)
        form = forms.AddProject(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            controller = Controller(uid=request.user.id,
                                    db_file=config.DATABASE_PATH)

            controller.add_project(title=title,
                                   description=description,
                                   members=[])

            return redirect('/polls/projects')
    else:
        form = forms.AddProject()

    return render(request, 'polls/add_project.html', {'form': form})


def vote(request, question_id):
    try:
        question = Question.get(Question.id == question_id)
    except DoesNotExist:
        raise Http404

    try:
        selected_choice = question.choice_set.where(
            Choice.id == int(request.POST['choice'])).get()
    except (KeyError, DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))

# Create your views here.
