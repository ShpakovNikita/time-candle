from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from .. import config
from . import shortcuts


def projects(request):
    if not request.user.is_authenticated:
        raise Http404
    controller = Controller(uid=request.user.id, db_file=config.DATABASE_PATH)
    projects_list = controller.get_projects('')[:5]

    context = {
        'projects_list': projects_list
    }
    try:
        redirect_view = shortcuts.project_card_post_form(
            request, controller, reverse('tc_web:projects'))
        if redirect_view:
            return redirect_view

        # convert all milliseconds fields to normal datetime.
        shortcuts.init_projects(request, controller, projects_list)

    except AppException as e:
        context['errors'] = e.errors.value

    return render(request, 'tc_web/projects/projects.html', context)


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

            return redirect(reverse('tc_web:projects'))
    else:
        form = forms.AddProject()

    return render(request, 'tc_web/projects/add_project.html', {'form': form})

