
celery -A src.infrastructure.celery_app.worker.celery_app worker --loglevel=info
celery -A src.infrastructure.celery_app.worker.celery_app beat --loglevel=info