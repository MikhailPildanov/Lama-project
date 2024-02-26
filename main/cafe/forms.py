from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'phone', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'phone']