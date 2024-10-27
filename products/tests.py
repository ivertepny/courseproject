from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from products.models import Product, ProductCategory
from products.views import ProductListView

pag_number = ProductListView.paginate_by


class IndexViewTestCase(TestCase):
    def test_index_view(self):
        path = reverse('index')
        template_name = 'products/index.html'
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Store')
        self.assertTemplateUsed(response, template_name=template_name)


class ProductsListViewTestCase(TestCase):
    # fixtures = ['categories_utf8.json', 'products_utf8.json']

    def setUp(self): # щоб не писати products = Product.objects.all() в кожному тесті
        self.products = Product.objects.all()
        # Create a category
        self.category = ProductCategory.objects.create(name="Category 1")

        # Create a dummy image for the product
        image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        # Create 10 products under this category with an image
        self.products = [
            Product.objects.create(
                name=f"Product {i}",
                category=self.category,
                price=10 + i,
                image=image  # Provide the dummy image
            )
            for i in range(10)
        ]

    def test_products_list_view(self):
        path = reverse('products:index')
        template_name = 'products/products.html'
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['object_list']), list(self.products[0:pag_number]))

    def test_products_list_view_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        # Fetch products dynamically from the database
        products_in_category = Product.objects.filter(category_id=category.id)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['object_list']),
            list(products_in_category[0:pag_number])  # Use the dynamic QuerySet here
        )

    def _common_tests(self, response): # щоб не повторювати код
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')

