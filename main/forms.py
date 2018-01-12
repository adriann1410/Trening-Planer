from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
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

    def save(self, user_id=-1):
        self.cleaned_data = dict([(k, v) for k, v in self.cleaned_data.items() if v != ""])
        update_user_model = get_object_or_404(User, id=user_id)
        if self.cleaned_data.get('first_name'):
            update_user_model.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name') is not None:
            update_user_model.last_name = self.cleaned_data['last_name']
        update_user_model.save()
        return super(UserUpdateForm, self).save(commit=False)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['old', 'weight', 'height']
        labels = {
            'old': "Age",
            'weight': "Weight",
            'height': "Height"
        }

    def save(self, user_id=-1):
        self.cleaned_data = dict([(k, v) for k, v in self.cleaned_data.items() if v != 0])
        print(self.cleaned_data)
        update_profile_model = get_object_or_404(User, id=user_id).profile
        if self.cleaned_data.get('old') is not None:
            update_profile_model.old = self.cleaned_data['old']
        if self.cleaned_data.get('weight') is not None:
            update_profile_model.weight = self.cleaned_data['weight']
        if self.cleaned_data.get('height') is not None:
            update_profile_model.height = self.cleaned_data['height']
        update_profile_model.save()
        return super(ProfileUpdateForm, self).save(commit=False)



class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

    def save(self, user_id=-1):
        self.cleaned_data = dict([(k, v) for k, v in self.cleaned_data.items() if v != ""])
        update_profile_model = get_object_or_404(User, id=user_id).profile
        if self.cleaned_data.get('image'):
            update_profile_model.image = self.cleaned_data['image']
        update_profile_model.save()
        return super(ProfileImageForm, self).save(commit=False)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 120, 'class': 'form-control col-md-8 col-sm-12 mr-4'}), label="")
    commentRate = forms.DecimalField(widget=forms.Select(
                                     choices=(('5', 5), ('4', 4), ('3', 3), ('2', 2), ('1', 1)),
                                     attrs={'class': 'form-control col-md-1 col-sm-12 ml-2'}),
                                     label="Ocena:",
                                     max_value=5,
                                     min_value=0,
                                     max_digits=2,
                                     decimal_places=1)
