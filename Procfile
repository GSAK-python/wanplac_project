web: gunicorn wanplac_project.wsgi --log-file -

celery: python manage.py celery -A wanplac_project worker --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler --loglevel=info -P solo