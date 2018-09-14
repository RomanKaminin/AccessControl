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
from app import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url, include



router = routers.DefaultRouter()
schema_view = get_swagger_view(title='Rest API for AccessControl')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^rest/registration/$', views.CreateUserView.as_view()),
    url(r'^rest/rest-auth/', include('rest_auth.urls')),
    url(r'^rest/send_request/', views.SendRequest.as_view()),
    url(r'^rest/access/(?P<pk>[0-9]+)/$', views.AccessDetail.as_view()),
    url(r'^rest/all_requests/', views.AllRequests.as_view()),
    url(r'^rest/auth/', views.AuthView.as_view(), name='auth-view'),
    url(r'^rest/docs/', schema_view)
]
