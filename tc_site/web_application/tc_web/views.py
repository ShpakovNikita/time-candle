from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from time_candle.model.time_formatter import get_datetime
from .models import Question, Choice
from time_candle.enums.status import Status
from . import config
from . import shortcuts
from django.contrib.auth.models import User
import json


def err404(request, exception):
    return render(
        request, 'polls/404.html', status=404)


def index(request):
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    return render(request, 'tc_web/index.html')


def profile(request, user_id):
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    try:
        django_user = User.objects.get(id=user_id)
        lib_user = controller.get_user(user_id)
    except (User.DoesNotExist, AppException):
        raise Http404

    screen_user = shortcuts.merge_instances(django_user, lib_user)

    return render(request, 'tc_web/profile.html', {'screen_user': screen_user})


def get_users(request):
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)

    if request.is_ajax():
        q = request.GET.get('term', '')
        re = '^' + q + '+'
        users = User.objects.filter(username__regex=re)
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def change_profile(request, user_id):
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    if request.user.id != user_id:
        raise Http404

    controller = Controller(uid=request.user.id,
                            db_file=config.DATABASE_PATH)

    if request.method == 'POST':
        print(request.POST)
        form = forms.ChangeProfileForm(request.POST)
        if form.is_valid():
            about = form.cleaned_data.get('about')
            nickname = form.cleaned_data.get('nickname')
            controller.change_user(user_id, nickname, about)

            return redirect(reverse('tc_web:profile', args=(user_id,)))

    else:
        form = forms.ChangeProfileForm()
        user = controller.get_user(user_id)
        form.fields['nickname'].widget.attrs.update({'value': user.nickname})
        form.fields['about'].widget.attrs.update({'value': user.about})

    return render(request, 'tc_web/change_profile.html', {'form': form})


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
