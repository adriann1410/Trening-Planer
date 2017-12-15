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
        labels = {
            'first_name': "Name",
            'last_name': "Surname"
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['old', 'weight', 'height']
        labels = {
            'old': "Age",
            'weight': "Weight",
            'height': "Height"
        }


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="")
    commentRate = forms.DecimalField(label="Ocena:", max_value=5, min_value=0, max_digits=2, decimal_places=1)

