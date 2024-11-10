from django.test import TestCase
from django.urls import reverse

from users.forms import UserRegistrationForm
from users.models import User  # , EmailVerification


class UserRegistrationViewTest(TestCase):

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.url = None

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

    def test_user_registration_post_failure(self):  # OK
        username = self.data['username']
        # user = User.objects.create_user(username=username)
        User.objects.create_user(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Користувач з таким ім\'ям вже існує.', html=True)
