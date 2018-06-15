from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
from django.urls import reverse
from time_candle.controller.commands import Controller
from time_candle.exceptions import AppException
from . import forms
from .. import config
from . import shortcuts
from tc_web import shortcuts as base
from django.contrib.auth.models import User


def projects(request):
    if not request.user.is_authenticated:
        return redirect('/login/')

    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

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
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    if request.method == 'POST':
        print(request.POST)
        form = forms.ProjectForm(request.POST)
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
        form = forms.ProjectForm()

    return render(request, 'tc_web/projects/add_project.html', {'form': form})


def change_project(request, project_id):
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {'errors': None}
    controller = Controller(uid=request.user.id,
                            db_file=config.DATABASE_PATH)

    if request.method == 'POST':
        print(request.POST)
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')
            if not description:
                description = None

            try:
                controller.change_project(project_id, title, description)

                return redirect(reverse('tc_web:projects'))
            except AppException as e:
                context['errors'] = e.errors.value
    else:
        form = forms.ProjectForm()

    context['form'] = form
    try:
        project = controller.get_project(project_id)
        context['project'] = project
        form.fields['title'].widget.attrs.update({'value': project.title})
        form.fields['description'].widget.attrs.update(
            {'placeholder': project.description})

    except AppException as e:
        raise Http404

    if request.user.id != project.admin_uid and not context['errors']:
        context['errors'] = 'You know that you cannot do that, right?'

    return render(request, 'tc_web/projects/change_project.html', context)


def add_user(request, project_id):
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}

    if request.method == 'POST':
        try:
            print(request.POST)
            try:
                if 'search_user' in request.POST \
                        and request.POST['search_user']:
                    user_id = User.objects.get(
                        username=request.POST['search_user']).id
                else:
                    user_id = None

            except User.DoesNotExist:
                errors = type('dummy', (), {})()
                errors.value = 'User does not exists'
                raise AppException(errors)

            controller = Controller(uid=request.user.id,
                                    db_file=config.DATABASE_PATH)

            controller.add_user_to_project(user_id, project_id)

            return redirect(reverse('tc_web:project', args=(project_id,)))
        except AppException as e:
            context['errors'] = e.errors.value

    return render(request, 'tc_web/projects/add_user.html', context)

