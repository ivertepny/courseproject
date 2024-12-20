from django.db import models
from django.apps import apps

# from products.models import Basket
from users.models import User


# Create your models here.

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'Створене'),
        (PAID, 'Сплачено'),
        (ON_WAY, 'В дорозі'),
        (DELIVERED, 'Доставлено'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order №{self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        basket = apps.get_model('products', 'Basket')
        baskets = basket.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'purchased_items': [basket.de_json() for basket in baskets],
            'total_sum': float(baskets.total_sum()),
        }
        baskets.delete()
        self.save()

    # для отримання текстового статусу в GoogleSheets
    def get_status_display(self):
        return dict(self.STATUSES).get(self.status, "Невідомий статус")
