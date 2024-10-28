from products.connect_mongodb import connect_mongo
from products.models import Product


# Оновлення кешу найпопулярніших продуктів у MongoDB

def update_popular_products_cache():
    popular_products = Product.popular.get_popular_products()  # Викликаємо метод менеджера
    if not popular_products:
        print("No popular products found.")
        return

    # Видаляємо старі записи
    result = connect_mongo().delete_many({})

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
        connect_mongo().insert_many(product_cache)
    # result = connect_mongo().insert_many(product_cache)
    else:
        print("No products to insert.")
