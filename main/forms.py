from django import forms
from django.contrib.auth.models import User
from .models import Comment

from .models import Profile

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100,required=True,  widget=forms.PasswordInput())


class UserForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=100)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['old', 'weight', 'height']

