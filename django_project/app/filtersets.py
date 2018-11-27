import django_filters
from app.models import AccessRequest


class AccessFilter(django_filters.FilterSet):

    class Meta:
        model = AccessRequest
        fields = ['access', 'space_name']

    def __init__(self, *args, **kwargs):
        super(AccessFilter, self).__init__(*args, **kwargs)
        self.filters['access'].label = "Текущий доступ"
        self.filters['space_name'].label = "Цель запроса"

