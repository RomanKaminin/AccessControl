from django.conf import settings


class BaseTemplate:
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL')


class NewRequestTemplate(BaseTemplate):
    subject = 'Новый запрос на получение доступа'
    message = 'Клиент {} запросил доступ в {}'
