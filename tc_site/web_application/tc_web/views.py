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
from .tasks import shortcuts


def err404(request, exception):
    return render(
        request, 'tc_web/404.html', status=404)


def index(request):
    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)
    latest_question_list = controller.get_tasks('')[:5]
    template = loader.get_template('tc_web/index.html')
    controller.get_tasks('tids: 10')

    context = {
        'latest_question_list': latest_question_list
    }
    return HttpResponse(template.render(context, request))


def profile(request, user_id):
    return render(request, 'tc_web/profile.html', {'screen_user': user_id})


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
        return render(request, 'tc_web/detail.html', {
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
            reverse('tc_web:results', args=(question.id,)))

# Create your views here.
