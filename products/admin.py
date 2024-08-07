from django.contrib import admin

# from . import models
# admin.site.register(models.Product)
# admin.site.register(models.ProductCategory)

from products.models import Product, ProductCategory, Tag, Basket

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Tag)
admin.site.register(Basket)




