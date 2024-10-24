import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'postcards_shop.settings')

app = Celery('postcards_shop')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
broker_connection_retry_on_startup = True


# Налаштовуємо періодичні задачі
app.conf.beat_schedule = {
    'update-popular-product-cache-every-day': {
        'task': 'products.tasks.update_popular_products_cache',
        'schedule': crontab('*/5'),  # Кожні 5 хвилин
    },
}
