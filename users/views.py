from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
# from django.contrib.auth.views import PasswordResetConfirmView
# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm, \
    UserPasswordChangeForm  # , UserPasswordResetForm
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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_no_social_user = True  # Mark as regular user
        user.save()
        return super().form_valid(form)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Кабінет'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])


class VerificationFailureView(TemplateView):
    template_name = 'users/email_verification_expired.html'


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
            user.delete()
            return HttpResponseRedirect(reverse_lazy('users:verification_failure'))


class UserPasswordChange(TitleMixin, PasswordChangeView):
    title = 'Store - Зміна пароля'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"

    # заборона зміни пароля якщо користувач авторизований через соціальну мережу
    def get(self, request, *args, **kwargs):
        if request.user.is_no_social_user:
            return super(UserPasswordChange, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('users:profile'))

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_no_social_user:
            messages.error(request, "You are not allowed to change your password from here.")
            return HttpResponseForbidden("You are not allowed to change your password from here.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)  # Оновлюємо сесію, щоб залишити користувача авторизованим
        return response

# class UserPasswordReset(TitleMixin, PasswordResetView):
#     title = 'Store - Скидання пароля'
#     model = User
#     form_class = UserPasswordResetForm
#     template_name = "users/password_reset_form.html"
#     email_template_name = "users/password_reset_email.html"
#     success_url = reverse_lazy("users:password_reset")
#
#     def form_valid(self, form):
#         messages.success(self.request, "На вашу електронну пошту надіслано лист для скидання пароля.")
#         return super().form_valid(form)
#
#
# class UserPasswordResetConfirm(TitleMixin, PasswordResetConfirmView):
#     title = 'Store - Підтвердження скидання пароля'
#     template_name = "users/password_reset_confirm.html"
#     success_url = reverse_lazy("users:password_reset_complete")
#     form_class = UserPasswordChangeForm  # Reusing UserPasswordChangeForm for setting new password
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         messages.success(self.request, "Ваш пароль успішно скинуто.")
#         return response
