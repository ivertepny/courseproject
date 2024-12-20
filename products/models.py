import stripe
from django.db import models

from users.models import User
from orders.models import Order
from django.conf import settings

# Create your models here.

stripe.api_key = settings.STRIPE_SECRET_KEY


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


# Менеджер для популярних продуктів

class PopularProductManager(models.Manager):
    def get_popular_products(self, limit=5):
        product_order_count = {}

        # Отримуємо всі замовлення зі статусом "Сплачено"
        orders = Order.objects.filter(status__gte=Order.PAID)
        for order in orders:
            for item in order.basket_history.get('purchased_items', []):
                # Перевіряємо, чи існує ключ 'product_id'
                product_id = item.get('product_id')

                if product_id:
                    if product_id in product_order_count:
                        product_order_count[product_id] += item['quantity']

                    else:
                        product_order_count[product_id] = item['quantity']

        # Сортуємо продукти за кількістю замовлень
        sorted_product_ids = sorted(product_order_count, key=product_order_count.get, reverse=True)[:limit]

        # Отримуємо продукти за відсортованими id
        products = list(self.filter(id__in=sorted_product_ids))

        # Сортуємо продукти відповідно до відсортованих id
        products_sorted = sorted(products, key=lambda product: sorted_product_ids.index(product.id))

        return products_sorted


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    stripe_product_price_id = models.CharField(max_length=100, null=True, blank=True)

    objects = models.Manager()
    popular = PopularProductManager()  # Додаємо кастомний менеджер

    # змінюємо назву в адмінці
    class Meta:
        verbose_name = 'Листівку'
        verbose_name_plural = 'Листівки'

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.stripe_product_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_product_price_id = stripe_product_price['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    # return f" {self.name} | Категорія: {self.category.name}"
    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='RON',
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity,
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()  # перевизначили метод object

    def __str__(self):
        return f"Кошик для {self.user.username} | Листівка: {self.product.name}"

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        basket_item = {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
        return basket_item

    @classmethod
    def create_or_update(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)

        if not baskets.exists():
            obj = Basket.objects.create(user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.first()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created
