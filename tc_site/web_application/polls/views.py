from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from time_candle.controller.commands import Controller

from .models import Question, Choice, DoesNotExist


def err404(request, exception):
    return render(
        request, 'polls/404.html', status=404)


def index(request):
    latest_question_list = Controller(uid=request.user.id, db_file='/home/shaft/repos/time-candle/time_candle/tc_site/web_application/data.db').get_tasks('')[:5]
    template = loader.get_template('polls/index.html')
    Controller(uid=request.user.id,
               db_file='/home/shaft/repos/time-candle/time_candle/tc_site/web_application/data.db').get_tasks(
        'tids: 10')

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

    tasks_list = Controller(uid=request.user.id - 1, db_file='/home/shaft/repos/time-candle/time_candle/tc_site/web_application/data.db').get_tasks('')[:5]

    context = {
        'tasks_list': tasks_list
    }

    return render(request, 'polls/tasks.html', context)


def projects(request):
    if not request.user.is_authenticated:
        raise Http404

    projects_list = Controller(uid=request.user.id, db_file='/home/shaft/repos/time-candle/time_candle/tc_site/web_application/data.db').get_projects('')[:5]

    context = {
        'projects_list': projects_list
    }

    return render(request, 'polls/projects.html', context)


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
