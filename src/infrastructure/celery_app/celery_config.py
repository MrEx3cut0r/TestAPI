from src.infrastructure.config.settings import settings


class CeleryConfig:    
    broker_url = settings.CELERY_BROKER_URL
    result_backend = settings.CELERY_RESULT_BACKEND
    
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'UTC'
    enable_utc = True
    
    beat_schedule = {
        'fetch-prices-every-minute': {
            'task': 'src.infrastructure.celery_app.tasks.fetch_market_prices_task',
            'schedule': 60.0, 
        },
    }
    
    broker_transport_options = {
        'visibility_timeout': 3600,
        'socket_keepalive': True,
        'retry_on_timeout': True,
    }