from django.conf.urls import url, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from . views import CreateUserView, SendRequest, AccessDetail, \
    AllRequests, AuthView


router = routers.DefaultRouter()
schema_view = get_swagger_view(title='Rest API for AccessControl')

urlpatterns = [
    url(r'^registration/$', CreateUserView.as_view(), name='api-registration'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^send_request/', SendRequest.as_view(), name='send-request'),
    url(r'^access/(?P<pk>[0-9]+)/$', AccessDetail.as_view()),
    url(r'^all_requests/', AllRequests.as_view()),
    url(r'^auth/', AuthView.as_view(), name='auth-view'),
    url(r'^docs/', schema_view)
]
