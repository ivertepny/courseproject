from pymongo import MongoClient

from postcards_shop import settings


def connect_mongo():  # Викликаємо функцію для оновлення кешу з MongoDB
    uri = settings.MONGO_DB_SETTINGS['URI']
    client = MongoClient(uri)
    db = client[settings.MONGO_DB_SETTINGS['DB_NAME']]
    collection = db[settings.MONGO_DB_SETTINGS['COLLECTION']]
    return collection
