from django.http import Http404
from django.shortcuts import (
    render,
    redirect,
)
from django.urls import reverse
from time_candle.exceptions import AppException
from tc_web.projects import forms
from tc_web.projects import shortcuts
from tc_web import shortcuts as base
from django.contrib.auth.models import User
from tc_web import logger


def projects(request):
    if not request.user.is_authenticated:
        logger.warning('user is not authenticated')
        return redirect('/login/')

    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    controller = base.get_controller(request)
    projects_list = controller.get_projects('')

    context = {
        'projects_list': projects_list
    }

    try:
        redirect_view = shortcuts.project_card_post_form(request, controller)

        # if we can redirect, then do it, else just render or render with errors
        # our template
        if redirect_view:
            logger.debug('redirect due to changes...')
            return redirect_view

        # adding some fields for better view
        shortcuts.init_projects(request, controller, projects_list)

    except AppException as e:
        context['errors'] = e.errors.value
        logger.warning(e.errors.value)

        # the errors doesn't
        shortcuts.init_projects(request, controller, projects_list)

    logger.debug('all projects rendered')
    return render(request, 'tc_web/projects/projects.html', context)


def add_project(request):
    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            controller = base.get_controller(request)

            controller.add_project(title=title,
                                   description=description,
                                   members=[])
            logger.debug('project added')

            return redirect(reverse('tc_web:projects'))

    else:
        form = forms.ProjectForm()

    return render(request, 'tc_web/projects/add_project.html', {'form': form})


def change_project(request, project_id):
    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {'errors': None}
    controller = base.get_controller(request)

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            description = form.cleaned_data.get('description')

            # if description if empty we pass it as not-to-change param
            if not description:
                description = None

            try:
                controller.change_project(project_id, title, description)
                logger.debug('project changed')

                return redirect(reverse('tc_web:projects'))
            except AppException as e:
                logger.debug(e.errors.value)
                context['errors'] = e.errors.value

    else:
        form = forms.ProjectForm()

    context['form'] = form

    # try because we can have some problems with rights when we try to visit
    # page
    try:
        project = controller.get_project(project_id)
        context['project'] = project
        form.fields['title'].widget.attrs.update({'value': project.title})
        form.fields['description'].widget.attrs.update(
            {'placeholder': project.description})

    except AppException as e:
        logger.warning(e.errors.value)
        raise Http404

    # if you are not admin and there was no errors for you before
    if request.user.id != project.admin_uid and not context['errors']:
        logger.debug('dont have rights for changing the project')
        context['errors'] = 'You know that you cannot do that, right?'

    return render(request, 'tc_web/projects/change_project.html', context)


def add_user(request, project_id):
    # we always init our search form
    for link in ['search']:
        redirect_link = base.search_user_forms(request, link)
        if redirect_link:
            return redirect_link

    context = {}
    controller = base.get_controller(request)

    if request.method == 'POST':

        # trying to add user to project
        try:
            # searching selected user in database
            try:
                if 'search_user' in request.POST \
                        and request.POST['search_user']:
                    user_id = User.objects.get(
                        username=request.POST['search_user']).id
                else:
                    user_id = None

            except User.DoesNotExist:
                # we need this for more elegant way to catch exception
                errors = type('dummy', (), {})()
                errors.value = 'User does not exists'
                logger.warning(errors.value)
                raise AppException(errors)

            controller.add_user_to_project(user_id, project_id)
            logger.debug('user to project was added')

            return redirect(reverse('tc_web:project', args=(project_id,)))

        except AppException as e:
            context['errors'] = e.errors.value

    # try because we can have some problems with rights when we try to visit
    # page
    try:
        project = controller.get_project(project_id)

    except AppException as e:
        logger.warning(e.errors.value)
        raise Http404

    # if you are not admin and there was no errors for you before
    if request.user.id != project.admin_uid and not context['errors']:
        context['errors'] = 'You know that you cannot do that, right?'

    return render(request, 'tc_web/projects/add_user.html', context)

