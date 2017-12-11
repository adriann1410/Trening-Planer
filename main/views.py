from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import  settings
from django.core.exceptions import ObjectDoesNotExist

from .forms import LoginForm, UserForm
from .models import CoachProfile, Profile, Comment

import socket


# Create your views here.
def index(request):
    return render(request, "index.html", context={'title':"Index"})

def coachesList(request):
    coaches = CoachProfile.objects.all()
    return render(request, "coaches.html", {'coaches':coaches})

def rate_coach(request):
    coach_id = request.POST.get('coach_id', None)
    rate = request.POST.get('rate', None)

    currentrate = 0
    if (coach_id):
        coach = CoachProfile.objects.get(user_id=int(coach_id))
        if coach is not None:
            coachrates = coach.rate_counter + 1
            currentrate = round((coach.rate_sum + float(rate)) / float(coachrates),1)
            coach.rate = currentrate
            coach.rate_sum = coach.rate_sum + float(rate)
            coach.rate_counter = coachrates
            coach.save()
    return HttpResponse(currentrate)


def userProfile(request, some_id):

    if CoachProfile.objects.filter(user_id=some_id).exists():
        coach = CoachProfile.objects.get(user_id=some_id)
        comments = reversed(Comment.objects.filter(user_id=some_id))
        return render(request, 'coachProfile.html', {'coach': coach, 'comments': comments})
    elif Profile.objects.filter(user_id=some_id).exists():
        user = Profile.objects.get(user_id=some_id)
        return render(request, "userProfile.html", {'page_user': user})
    else:
        return HttpResponse("Użytkownik nie istnieje")


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
            return redirect(index)
    else:
        form = LoginForm()

    return render(request, "login.html", context={'title':"Login", 'form': form})


def registerView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(email=cd.get('email'))
                if user:
                    message = "Email already in use xd"
                    return render(request, "register.html", context={'title': "Register", 'form': form, 'message':message})
            except User.DoesNotExist as e:
                pass
            password = make_password(cd.get('password'))

            new_user = User(email=cd.get('email'), password=password, username=cd.get('email'))
            new_user.save()
            subject = "Dziękujemy za rejestrację w Planer"
            mail_message = "Tutaj bedzie link do potwierdzenia konta"
            # socket.getaddrinfo('127.0.0.1', 8000)
            send_mail(subject, mail_message, settings.EMAIL_HOST_USER, [cd.get('email')], fail_silently=True)

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

