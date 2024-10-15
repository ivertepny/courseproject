from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, \
    PasswordResetForm
from django import forms
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField

from users.models import User
from users.tasks import send_email_verification


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()


class UserLoginForm(AuthenticationForm):
    captcha = ReCaptchaField()
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я користувача"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': 'Введіть пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        super().clean()  # Call the parent class's clean method
        username = self.cleaned_data.get('username')

        try:
            user = User.objects.get(username=username)
            if not user.is_verified_email:
                raise ValidationError("Ваш аккаунт не авторизовано. Будь ласка перевірте свою пошту і авторизуйтесь.")
        except User.DoesNotExist:
            raise ValidationError("Такого користувача і пароля не існує")

        return self.cleaned_data


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть фамілію"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть ім'я користувача"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть адресу електронної пошти"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Повторіть пароль"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    # додаємо верифікацію пошти
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        # send_email_verification(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старий пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новий пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Підтвердження пароля",
                                    widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class UserPasswordResetForm(PasswordResetForm):

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Введіть адресу електронної пошти"}))

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        super().clean()  # Call the parent class's clean method
        email = self.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)
            if not user.is_verified_email:
                raise ValidationError("Ваш аккаунт не авторизовано. Будь ласка перевірте свою пошту і авторизуйтесь.")
        except User.DoesNotExist:
            raise ValidationError("Такого користувача і пароля не існує")

        return self.cleaned_data
