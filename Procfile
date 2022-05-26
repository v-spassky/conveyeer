release: chmod u+x pictor/font_setup.sh && pictor/font_setup.sh
web: gunicorn run:app
worker: celery -A adiutor.celery worker --loglevel=INFO
