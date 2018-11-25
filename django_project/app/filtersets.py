import django_filters
from app.models import AccessRequest


class AccessFilter(django_filters.FilterSet):

    class Meta:
        model = AccessRequest
        fields = ['access', 'space_name']



