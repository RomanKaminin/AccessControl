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
from django.contrib.auth import views as auth_views
from app.views import (HomePageView, AccessesList,
                       logout_user, LoginView, RegisterView,
                       AccessEdit, AccessesCreate, AlphaList)


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include('app.api.urls')),
    url(r'^$', HomePageView.as_view(),name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout$', logout_user, name='logout'),
    url(r'^accesses/$', AccessesList.as_view(), name='accesses'),
    url(r'^accesses/new_access$', AccessesCreate.as_view(), name='new-access'),
    url(r'^registration/$', RegisterView.as_view(), name='registration'),
    url(r'^accesses/access/(?P<pk>\d+)/$', AccessEdit.as_view(), name='edit-access'),
    url(r'^alphabetical_index$', AlphaList.as_view(), name='alphabetical-index'),
    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^user/password/reset/$', auth_views.PasswordResetView.as_view(),
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done"),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(),
        {'post_reset_redirect' : '/user/password/done/'},
        name="auth_password_reset_confirm"),
    url(r'^user/password/done/$', auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete"),
]
