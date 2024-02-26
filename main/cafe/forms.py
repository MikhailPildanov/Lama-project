from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone=phone):
            raise ValidationError("Этот адрес электронной почты уже существует.")
        return phone
