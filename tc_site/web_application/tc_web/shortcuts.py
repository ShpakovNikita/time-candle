from copy import copy
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


def merge_instances(obj_1, obj_2):
    buff_obj = copy(obj_1)
    for key, value in obj_2.__dict__.items():
        setattr(buff_obj, key, value)

    return buff_obj


def search_user_forms(request, search_field='search', redirect_flag=True):
    if request.method == "GET":
        if search_field in request.GET:

            profile_uid = User.objects.get(
                username=request.GET[search_field]).id

            if redirect_flag:
                return redirect(reverse('tc_web:profile', args=(profile_uid,)))
            else:
                return profile_uid
