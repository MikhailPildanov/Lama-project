from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField()

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField()

    class Meta:
        model = Customer
        fields = ['name', 'phone']