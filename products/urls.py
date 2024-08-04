# Мій файл urls

from django.urls import path

from products.views import products

app_name = 'products' # Не зрозумів для чого

urlpatterns = [
    path('', products, name='index'),
]

