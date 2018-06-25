"""time_candle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from main_system import (
    views,
    startup,
)
from . import settings
import django.views.static

handler404 = 'tc_web.views.err404'
handler500 = 'tc_web.views.err500'

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='logout'),
    url(r'^signup/$', views.signup, name='signup'),

    path('tc_web/', include('tc_web.urls')),
    path('admin/', admin.site.urls),
    path('', views.index)
]

if not settings.DEBUG:
    urlpatterns.append(path('static/<path>.', django.views.static.serve,
                            {'document_root': settings.STATIC_ROOT}))


startup.start_up()
