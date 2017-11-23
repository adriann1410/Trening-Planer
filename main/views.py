from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.hashers import make_password

from .forms import  LoginForm, UserForm

# Create your views here.
def index(request):
    return render(request, "index.html", context={'title':"Index"})


def loginView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.get(email=email)

            if not user.check_password(password):
                message = "Password is not correct"
                return render(request, "login.html", context={'title':"Login", 'form': form, 'message': message})

            login(request, user)
            return redirect(users)
    else:
        form = LoginForm()

    return  render(request, "login.html", context={'title':"Login", 'form': form})

def registerView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(email=cd.get('email'))
                if user:
                    message = "Email already in use"
                    return render(request, "register.html", context={'title': "Register", 'form': form, 'message':message})
            except User.DoesNotExist as e:
                pass
            password = make_password(cd.get('password'))

            new_user = User(email=cd.get('email'), password=password)
            new_user.save()
    #       mail.send(email=cd.get('email'))

    else:
        form = UserForm
    return render(request, "register.html", context={'title':"Register", 'form': form})


@login_required
def users(request):
    all_users = User.objects.all()
    return render(request, "users.html", context={'title':"Users", 'users': all_users})

@login_required
def logoutView(request):
    logout(request)
    return redirect(loginView)
