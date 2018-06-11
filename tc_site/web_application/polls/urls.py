from django.urls import path
from . import startup
from . import views
from .tasks import views as task_views
from .projects import views as project_views


app_name = 'polls'


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('tasks/', task_views.tasks, name='tasks'),
    path('projects/', project_views.projects, name='projects'),

    path('tasks/add_task/', task_views.add_task, name='add_task'),
    path('tasks/add_task/<int:project_id>/',
         task_views.add_project_task,
         name='add_project_task'),
    path('projects/add_project/',
         project_views.add_project,
         name='add_project'),

    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('project/<int:project_id>', task_views.project, name='project'),
    path('profile/<int:user_id>', views.profile, name='profile'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

startup.startup()
