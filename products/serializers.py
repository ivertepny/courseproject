from rest_framework import serializers
from rest_framework import fields

from users.models import User
from products.models import Product, Basket

user = User.objects.first()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name',)


# ProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    # display_name = serializers.SerializerMethodField()

    # def get_display_name(self, obj: Product):
    #     display_name = obj.name
    #
    #     return display_name

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category', 'tags')


# BasketSerializer

class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_sum', 'total_quantity', 'created_timestamp')
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()
