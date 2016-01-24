from celery import Celery

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

celery = Celery(
    'proj',
    broker=BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)


@celery.task
def add(a, b):
    return a + b
