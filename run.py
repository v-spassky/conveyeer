from celery import current_app
from celery.bin import worker
from adiutor import app
from pictor import pictor
from lector import lector

"""
Launches web server on a specified port.
"""

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

    application = current_app._get_current_object()
    worker = worker.worker(app=application)
    options = {
        'broker': app.config['CELERY_BROKER_URL'],
        'loglevel': 'INFO',
        'traceback': True,
    }

    worker.run(**options)
