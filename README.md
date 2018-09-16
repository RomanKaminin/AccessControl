* docker-compose build
* docker-compose up --remove-orphans
* python manage.py createsuperuser --email admin@example.com --username admin


1. перед регистрацией пользователей в админке приложения необходимо создать 2 группы ('managers' и 'clients') иначе запросы не пройдут
2. Для того чтобы пользователь мог редактировать или удалять (его через web админку нужно добавить в группу 'managers')
3. For check API use curl
