"""access_control URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from app.views import HomePageView, get_accesses, \
     logout_user, LoginView, add_access, RegisterView, \
    access_detail


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include('app.api.urls')),
    url(r'^$', HomePageView.as_view(),name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout$', logout_user, name='logout'),
    url(r'^accesses/$', get_accesses, name='accesses'),
    url(r'^accesses/new_access$', add_access, name='new-access'),
    url(r'^registration/$', RegisterView.as_view(), name='registration'),
    url(r'^accesses/access/(?P<pk>\d+)/$', access_detail, name='access-detail'),
]
