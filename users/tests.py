from django.test import TestCase
from django.urls import reverse

from datetime import timedelta
from django.utils.timezone import now

from users.forms import UserRegistrationForm
from users.models import User, EmailVerification


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'firs_name': 'Ivan',
            'last_name': 'Pupkin',
            'username': 'pepa83',
            'email': 'igor@gohard.ua',
            'password1': 'c34s8Hq8xa04844',
            'password2': 'c34s8Hq8xa04844'
        }

    def test_user_registration_get(self):  # OK
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['title'], 'Store - Реєстрація')
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertIsInstance(response.context_data['form'], UserRegistrationForm)

    def test_user_registration_post_success(self):  # Error
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user object
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=username).exists())
        self.assertEqual(response.url, reverse('users:login'))

        # check creating e-mail verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(minutes=10)).date()
        )

    def test_user_registration_post_failure(self):  # OK
        username = self.data['username']
        user = User.objects.create_user(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Користувач з таким ім\'ям вже існує.', html=True)
