web: gunicorn basewave.wsgi:application
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput