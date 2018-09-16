* docker-compose build
* docker-compose up --remove-orphans
* docker-compose run --rm django_project python ./manage.py createsuperuser --email admin@example.com --username admin


1. Before start registration users create 2 Groups ('managers' и 'clients') 
2. For delete or change  message, user must is included in the group 'managers' (from admin panel included user in 'managers')
3. For check API use curl
