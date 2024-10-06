import graphene
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from orders.models import Order
from products.models import Product


class ProductObjectType(DjangoObjectType):
    class Meta:
        model = Product
        filter_fields = ('id', 'name', 'price')
        interfaces = (graphene.relay.Node,)


class OrderProductObjectType(DjangoObjectType):
    class Meta:
        model = Order
        filter_fields = ('product', 'quantity', 'price')


class OrderObjectType(DjangoObjectType):
    order_products = graphene.List(OrderProductObjectType)

    class Meta:
        model = Order
        fields = ('id', 'user', 'total_quantity', 'order_products')
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    # hello = graphene.String(default_value="Hi!")

    products = DjangoFilterConnectionField(ProductObjectType)
    orders = graphene.List(OrderObjectType)

    def resolve_orders(self, info):
        return Order.objects.all()

    # def resolve_products(self, info):
    #     return Product.objects.all()


schema = graphene.Schema(query=Query)
