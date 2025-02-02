from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserSignupForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, help_text='Usename required.')
    user_type = forms.CharField(max_length=50, required=True, help_text='User type required')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','user_type', )