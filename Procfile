web: gunicorn ielts.wsgi
web:python manage.py runserver 0.0.0.0:5000
python manage.py collectstatic --noinput
manage.py migrate