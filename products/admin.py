from django.contrib import admin

# from . import models
# admin.site.register(models.Product)
# admin.site.register(models.ProductCategory)

from products.models import Product, ProductCategory, Tag, Basket

# admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Tag)


# admin.site.register(Basket)


# тюнінг адмін-панелі
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category', 'tags')
    search_fields = ('name',)
    ordering = ('name',)


# вставляємо кошив в юзера (TabularInline коли є foreignkey)
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity', 'created_timestamp')
    extra = 0
    readonly_fields = ('created_timestamp',) # інакше буде помилка
