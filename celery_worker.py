from app import create_app
from extensions import celery
from config import config
from celery import Celery
flask_app = create_app()
flask_app.app_context().push()

celery = Celery(
    __name__,
    broker=flask_app.config['CELERY_BROKER_URL'],
    backend=flask_app.config['CELERY_RESULT_BACKEND']
)

celery.conf.update(flask_app.config)

