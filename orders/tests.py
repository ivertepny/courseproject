import hashlib
import hmac
import time
import json

from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from unittest.mock import patch

from django.contrib.auth import get_user_model
from orders.models import Order
from products.models import Basket, Product, ProductCategory

User = get_user_model()


class OrderViewsTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        # Create a test product category and product for testing
        self.category = ProductCategory.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Product Description',
            price=100,
            quantity=10,
            category=self.category
        )

    def test_order_create_view(self):  # OK
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order-create.html')

    def test_order_create_view_post_success(self):  # OK

        # Create a test basket for the user
        Basket.objects.create(user=self.user, product=self.product, quantity=2)

        response = self.client.post(reverse('orders:order_create'), data={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '123 Test Street',
        })

        self.assertEqual(response.status_code, 303)
        self.assertTrue(Order.objects.filter(email='john.doe@example.com').exists())

    def test_order_success_view(self):  # Error
        response = self.client.get(reverse('orders:order_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/success.html')

    def test_order_canceled_view(self):  # Error
        response = self.client.get(reverse('orders:order_canceled'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/canceled.html')

    def test_order_list_view(self):
        response = self.client.get(reverse('orders:orders_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/orders.html')

    def test_order_detail_view(self):
        order = Order.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            address='123 Test Street',
            initiator=self.user,
            status=Order.PAID
        )

        response = self.client.get(reverse('orders:order', args=[order.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/order.html')

    def test_send_orders_to_google_sheet_view(self):  # OK

        response = self.client.get(reverse('orders:send_to_google_sheet'))
        self.assertEqual(response.status_code, 302)  # Should redirect to Google Sheet URL


class StripeWebhookViewTests(TestCase):
    @patch('orders.views.fulfill_order')  # Replace with the actual import path
    @patch('orders.views.send_telegram.delay')  # Replace with the actual import path
    def test_stripe_webhook_valid_event(self, mock_send_telegram, mock_fulfill_order):
        # Mock the Stripe event
        event_data = {
            'id': 'evt_test_webhook',
            'object': 'event',
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_session_id',
                    'amount_total': 1000,
                    'currency': 'usd',
                    # Include other necessary fields here if needed
                }
            }
        }

        # Create a valid signature
        sig_header = self.create_valid_signature(event_data)

        # Call the view with the mocked event
        response = self.client.post(
            reverse('stripe_webhook'),  # Update with your URL name
            data=json.dumps(event_data),  # Send as JSON
            content_type='application/json',
            **{'HTTP_STRIPE_SIGNATURE': sig_header}
        )

        # Check the response status
        self.assertEqual(response.status_code, 200)

        # Verify that the fulfill_order and send_telegram were called
        mock_fulfill_order.assert_called_once_with(event_data['data']['object'])
        mock_send_telegram.assert_called_once()

    def test_stripe_webhook_invalid_payload(self):
        # Call the view with an invalid payload
        response = self.client.post(
            reverse('stripe_webhook'),  # Update with your URL name
            data='invalid_payload',
            content_type='application/json',
            **{'HTTP_STRIPE_SIGNATURE': 'invalid_signature'}
        )

        # Check the response status
        self.assertEqual(response.status_code, 400)

    def test_stripe_webhook_invalid_signature(self):
        # Mock the Stripe event
        event_data = {
            'id': 'evt_test_webhook',
            'type': 'checkout.session.completed',
            'data': {
                'object': {
                    'id': 'cs_test_session_id',
                }
            }
        }

        # Call the view with an invalid signature
        response = self.client.post(
            reverse('stripe_webhook'),  # Update with your URL name
            data=json.dumps(event_data),  # Send as JSON
            content_type='application/json',
            **{'HTTP_STRIPE_SIGNATURE': 'invalid_signature'}
        )

        # Check the response status
        self.assertEqual(response.status_code, 400)

    def create_valid_signature(self, event_data):
        """Generate a valid Stripe webhook signature."""
        payload = json.dumps(event_data)
        timestamp = str(int(time.time()))  # Use the current timestamp
        signature = hmac.new(
            settings.STRIPE_WEBHOOK_SECRET.encode(),
            f"{timestamp}.{payload}".encode(),
            hashlib.sha256
        ).hexdigest()

        return f't={timestamp},v1={signature}'  # Format the signature header
