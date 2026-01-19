from celery import Celery
from .celery_config import CeleryConfig


def create_celery_app():
    celery_app = Celery('crypto_price_tracker')
    celery_app.config_from_object(CeleryConfig)
    
    celery_app.autodiscover_tasks([
        'src.infrastructure.celery_app.tasks'
    ])
    
    return celery_app


celery_app = create_celery_app()