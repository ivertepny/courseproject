# tests.py
import graphene
from django.test import TestCase
from graphene_django.utils import GraphQLTestCase
from products.models import Product, ProductCategory, Basket  # Update the import path if necessary
from orders.models import Order  # Update the import path if necessary
from users.models import User  # Update the import path if necessary
from .schema import schema  # Import your GraphQL schema


class ProductQueryTests(GraphQLTestCase):
    schema = schema

    def setUp(self):
        # Create a sample category
        self.category = ProductCategory.objects.create(name="Sample Category")

        # Create sample products with category
        self.product1 = Product.objects.create(name="Product 1", price=10.0, category=self.category)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, category=self.category)

    def test_query_products(self):
        query = '''
        query {
            products {
                edges {
                    node {
                        id
                        name
                        price
                    }
                }
            }
        }
        '''
        response = self.query(query)
        self.assertResponseNoErrors(response)

        products = response.json()['data']['products']['edges']
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['node']['name'], self.product1.name)
        self.assertEqual(products[1]['node']['name'], self.product2.name)


# class OrderQueryTests(GraphQLTestCase):
#     schema = schema
#
#     def setUp(self):
#         # Create a sample category and product
#         self.category = ProductCategory.objects.create(name="Sample Category")
#         self.product = Product.objects.create(name="Product 1", price=10.0, category=self.category)
#
#         # Create a user or a valid initiator for the order
#         self.initiator = User.objects.create(username="testuser")  # Assuming User is your user model
#
#         # Create an order with a valid initiator_id
#         self.order = Order.objects.create(initiator_id=self.initiator.id)  # Use the initiator's ID
#
#         # Link product to the order
#         self.order.order_products.create(product=self.product, quantity=2, price=self.product.price)
#
#     def test_query_orders(self):
#         query = '''
#         query {
#             orders {
#                 id
#                 orderProducts {
#                     product {
#                         id
#                         name
#                     }
#                     quantity
#                     price
#                 }
#             }
#         }
#         '''
#         response = self.query(query)
#         self.assertResponseNoErrors(response)
#
#         orders = response.json()['data']['orders']
#         self.assertEqual(len(orders), 1)
#         self.assertEqual(orders[0]['orderProducts'][0]['product']['name'], self.product.name)
