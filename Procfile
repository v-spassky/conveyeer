release: chmod u+x pictor/font_setup.sh && pictor/font_setup.sh
web: gunicorn app:run
worker: celery -A adiutor.celery worker --loglevel=INFO
