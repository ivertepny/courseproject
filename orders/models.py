from django.db import models
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
    status = models.SmallIntegerField(choices=STATUSES, default=CREATED)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order # {self.id}. {self.first_name} {self.last_name}'
