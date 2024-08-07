from django.db import models

from users.models import User


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    # return f" {self.name} | Категорія: {self.category.name}"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
        # return f" Кошик для {self.user.email} | Продукт: {self.product.name}"
