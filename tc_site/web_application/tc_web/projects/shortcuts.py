from django.shortcuts import redirect
from tc_web import logger


# use this function if you have post forms in your page
def project_card_post_form(request, controller, redirect_link):
    if request.method == 'POST':
        logger.debug(request.POST)
        if 'delete' in request.POST:
            controller.remove_project(request.POST['delete'])
            return redirect(redirect_link)


# just add some fields to the base projects for better user experience and
# showing more clean data
def init_projects(request, controller, projects_list):
    for project in projects_list:
        if project.admin_uid == request.user.id:
            project.admin_name = 'You'
        else:
            project.admin_name = controller.get_user(project.admin_uid).login
