# Мій файл urls

from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductListView, basket_add, basket_remove, basket_update, ProductSearchListView, \
    PopularProductsView

app_name = 'products' # Не зрозумів для чого

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    # кеш всієї сторінки
    # path('', cache_page(30)(ProductListView.as_view()), name='index'),
    path('category/<int:category_id>/', ProductListView.as_view(), name='category'),
    path('page/<int:page>', ProductListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('basket/update/<int:basket_id>/', basket_update, name='basket_update'),
    path('search/', ProductSearchListView.as_view(), name='custom_search'),
    path('popular/', PopularProductsView.as_view(), name='popular_products'),
]

