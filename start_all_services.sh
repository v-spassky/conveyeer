#!/bin/bash

# Handles spinning up Redis, Celery and web server.

redis-server &
celery -A adiutor.celery worker --loglevel=INFO &
gunicorn run:app