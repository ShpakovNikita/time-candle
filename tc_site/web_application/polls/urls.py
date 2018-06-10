from django.urls import path
from . import startup
from . import views


app_name = 'polls'


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('tasks/', views.tasks, name='tasks'),
    path('projects/', views.projects, name='projects'),

    path('tasks/add_task/', views.add_task, name='add_task'),
    path('tasks/add_task/<int:project_id>/',
         views.add_project_task,
         name='add_project_task'),
    path('projects/add_project/', views.add_project, name='add_project'),

    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('project/<int:project_id>', views.project, name='project'),
    path('profile/<int:user_id>', views.profile, name='profile'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

startup.startup()
