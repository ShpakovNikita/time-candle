from django.urls import path
from . import startup
from . import views


app_name = 'polls'


urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),

    path('tasks/', views.tasks, name='tasks'),
    path('projects/', views.projects, name='projects'),

    path('add_task/', views.add_task, name='add_task'),
    path('add_project/', views.add_project, name='add_project'),

    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

startup.startup()
