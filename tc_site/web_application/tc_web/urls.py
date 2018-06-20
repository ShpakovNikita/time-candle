from django.urls import path
from django.conf.urls import include, url
from tc_web import startup
from tc_web import views
from tc_web.tasks import views as task_views
from tc_web.projects import views as project_views


app_name = 'tc_web'


urlpatterns = [
    path('', views.index, name='index'),

    path('tasks/', task_views.tasks, name='tasks'),
    path('projects/', project_views.projects, name='projects'),

    path('tasks/add_task/', task_views.add_task, name='add_task'),
    path('tasks/<int:project_id>/add_task/',
         task_views.add_task,
         name='add_project_task'),
    path('tasks/<int:project_id>/add_task/<int:task_id>/',
         task_views.add_task,
         name='add_child_project_task'),
    path('tasks/add_task/<int:task_id>/',
         task_views.add_task,
         name='add_child_task'),
    path('tasks/change_task/<int:task_id>/',
         task_views.change_task,
         name='change_task'),
    path('tasks/show_task/<int:task_id>/',
         task_views.show_task,
         name='show_task'),

    path('projects/add_project/',
         project_views.add_project,
         name='add_project'),

    path('project/<int:project_id>/', task_views.project, name='project'),
    path('project/<int:project_id>/add_user',
         project_views.add_user,
         name='add_user'),
    path('projects/change_project/<int:project_id>/',
         project_views.change_project,
         name='change_project'),

    path('profile/id<int:user_id>/', views.profile, name='profile'),
    path('profile/change_profile/<int:user_id>/',
         views.change_profile,
         name='change_profile'),

    url(r'^api/get_users/', views.get_users, name='get_users'),
    path('api/get_project_users/<int:project_id>/',
         views.get_project_users,
         name='get_project_users')
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

# one time on runserver startup function
startup.start_up()
