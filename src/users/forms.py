from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from typing import Type, List


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model: Type[User] = User
        fields: List[str] = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model: Type[User] = User
        fields: List[str] = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model: Type[Profile] = Profile
        fields: List[str] = ['image']
