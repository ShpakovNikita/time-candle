from django.http import (
    HttpResponse,
    Http404,
)
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from tc_web import forms
from tc_web import config
from tc_web import shortcuts
from django.contrib.auth.models import User
import json


def err404(request, exception):
    return render(
        request, 'polls/404.html', status=404)


def index(request):
    # we always init our search form
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    return render(request, 'tc_web/index.html')


def profile(request, user_id):
    # we always init our search form
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    try:
        django_user = User.objects.get(id=user_id)
        lib_user = controller.get_user(user_id)
    except (User.DoesNotExist, AppException):
        raise Http404

    # merge two user objects to get one full user info
    screen_user = shortcuts.merge_instances(django_user, lib_user)

    return render(request, 'tc_web/profile.html', {'screen_user': screen_user})


# function for autocomplete user search
def get_users(request):
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


# function for autocomplete project user search
def get_project_users(request, project_id):
    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = controller.get_users(project_id)
        users = [user for user in users if user.login.startswith(q)]
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.uid
            user_json['label'] = user.login
            user_json['value'] = user.login
            results.append(user_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def change_profile(request, user_id):
    # we always init our search form
    for link in ['search']:
        redirect_link = shortcuts.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    if request.user.id != user_id:
        raise Http404

    controller = Controller(uid=request.user.id,
                            psql_config=config.DATABASE_CONFIG)

    if request.method == 'POST':
        form = forms.ChangeProfileForm(request.POST)
        if form.is_valid():
            about = form.cleaned_data.get('about')
            nickname = form.cleaned_data.get('nickname')
            controller.change_user(user_id, nickname, about)

            return redirect(reverse('tc_web:profile', args=(user_id,)))

    else:
        form = forms.ChangeProfileForm()
        user = controller.get_user(user_id)

        # init fields with default values
        form.fields['nickname'].widget.attrs.update({'value': user.nickname})
        form.fields['about'].widget.attrs.update({'value': user.about})

    return render(request, 'tc_web/change_profile.html', {'form': form})
