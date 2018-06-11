from django.shortcuts import redirect


def project_card_post_form(request, controller, redirect_link):
    if request.method == 'POST':
        if 'delete' in request.POST:
            controller.remove_project(request.POST['delete'])
            return redirect(redirect_link)


def init_projects(request, controller, projects_list):
    for project in projects_list:
        if project.admin_uid == request.user.id:
            project.admin_name = 'You'
        else:
            project.admin_name = controller.get_user(project.admin_uid).login
