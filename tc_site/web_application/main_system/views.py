from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, reverse
from . import models
from . import forms
from time_candle.controller.commands import Controller
from tc_web import config


def signup(request):
    if request.method == 'POST':
        controller = Controller(uid=request.user.id,
                                db_file=config.DATABASE_PATH)

        print(request.POST)
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            controller.add_user(username)

            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/tc_web/')
    else:
        form = forms.SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    return redirect(reverse('tc_web:index'))
