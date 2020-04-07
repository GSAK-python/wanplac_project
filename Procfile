web: gunicorn wanplac_project.wsgi --log-file -
worker: celery -A wanplac_project  worker --loglevel=info -P solo
beat: celery -A wanplac_project beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler