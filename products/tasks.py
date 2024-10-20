from celery import shared_task
from products.cache_utils import update_popular_products_cache as update_cache


@shared_task
def update_popular_products_cache():
    update_cache()
