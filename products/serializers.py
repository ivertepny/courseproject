from rest_framework import serializers
from rest_framework import fields

from products.models import Product, ProductCategory, Tag, Basket


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category', 'tags')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.FloatField(required=False)
    total_sum = fields.SerializerMethodField()
    total_quantity = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'created_timestamp', 'sum', 'total_sum', 'total_quantity')
        read_only_fields = ('created_timestamp',)

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user_id).total_sum()

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user_id).total_quantity()
