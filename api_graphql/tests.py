from graphene_django.utils import GraphQLTestCase
from products.models import Product, ProductCategory
from .schema import schema


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
