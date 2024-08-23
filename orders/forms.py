from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "Ім'я"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "Фамілія"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': "Електронна пошта"}))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': "Адреса"}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
