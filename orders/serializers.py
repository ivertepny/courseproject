from rest_framework import serializers
from rest_framework import fields

from orders.models import Order
from users.models import User

user = User.objects.first()


# OrderViewSerializer

class OrderSerializer(serializers.ModelSerializer):
    initiator = serializers.StringRelatedField()
    basket_history = fields.JSONField()

    class Meta:
        model = Order
        fields = ('id', 'initiator', 'basket_history')
