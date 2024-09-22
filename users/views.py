from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, UserPasswordChangeForm
from users.models import User, EmailVerification
from common.views import TitleMixin


# Create your views here.
class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизація'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вітаємо! Ви успішно зареєеструвались'
    title = 'Store - Реєстрація'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Кабінет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])


# використовуємо context_processors

# def get_context_data(self, **kwargs):
#     context = super(UserProfileView, self).get_context_data()
#     context['baskets'] = Basket.objects.filter(user=self.object)
#     return context


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - підтвердження електронної пошти'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
