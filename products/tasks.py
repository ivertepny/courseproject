from celery import shared_task
from pymongo import MongoClient
from django.conf import settings
from products.models import Product

# URI для підключення до MongoDB
uri = settings.MONGO_DB_SETTINGS['URI']
# Створення клієнта MongoDB через URI
client = MongoClient(uri)

# Вибір бази даних і колекції
db = client[settings.MONGO_DB_SETTINGS['DB_NAME']]
collection = db[settings.MONGO_DB_SETTINGS['COLLECTION']]


# Оновлення кешу найпопулярніших продуктів у MongoDB
@shared_task
def update_popular_products_cache():
    popular_products = Product.objects.get_popular_products()  # Викликаємо метод менеджера
    if not popular_products:
        print("No popular products found.")
        return

    # Видаляємо старі записи
    result = collection.delete_many({})

    # Вставляємо нові продукти в кеш
    product_cache = []
    for product in popular_products:
        product_cache.append({
            'product_id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),
        })

    if product_cache:
        result = collection.insert_many(product_cache)

    else:
        print("No products to insert.")
