from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100,required=True,  widget=forms.PasswordInput())
    #     if not user:
    #         raise forms.ValidationError("User does not exist")
    #
    #     if not user.check_password(password):
    #         raise  forms.ValidationError("Password is not correct")
    #
    #     if not user.is_active():
    #         raise forms.ValidationError("User is not active")


class UserForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True, max_length=100)

