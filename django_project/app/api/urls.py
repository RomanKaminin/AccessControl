from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from . views import CreateUserView, SendRequest, AccessDetail, \
    AllRequests, AuthView


router = routers.DefaultRouter()
schema_view = get_swagger_view(title='Rest API for AccessControl')

urlpatterns = [
    url(r'^access_control/registration/$', CreateUserView.as_view()),
    url(r'^access_control/rest-auth/', include('rest_auth.urls')),
    url(r'^access_control/send_request/', SendRequest.as_view()),
    url(r'^access_control/access/(?P<pk>[0-9]+)/$', AccessDetail.as_view()),
    url(r'^access_control/all_requests/', AllRequests.as_view()),
    url(r'^access_control/auth/', AuthView.as_view(), name='auth-view'),
    url(r'^access_control/docs/', schema_view)
]
