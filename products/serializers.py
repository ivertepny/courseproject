from rest_framework import serializers

from products.models import Product, ProductCategory, Tag


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=ProductCategory.objects.all())
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category', 'tags', 'image')

