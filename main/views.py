from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from  django.contrib.auth import login, logout, authenticate, get_user_model

from .forms import  LoginForm
from .models import CoachProfile

# Create your views here.
def index(request):
    return render(request, "index.html", context={'title':"Index"})

def coachesList(request):
    coaches = CoachProfile.objects.all()
    return render(request, "coaches.html", {'coaches':coaches})

def rate_coach(request):
    coach_id = request.GET.get('coach_id', None)
    rate = request.GET.get('rate', None)

    currentrate = 0
    if (coach_id):
        coach = CoachProfile.objects.get(user_id=int(coach_id))
        if coach is not None:
            coachrates = coach.rate_counter +1
            currentrate = round((coach.rate + rate) / coachrates,1)
            print(currentrate)
            coach.rate = currentrate
            coach.rate_counter = coachrates
            coach.save()
    return HttpResponse(currentrate)

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

    return  render(request, "login.html", context={'title':"Login", 'form': form})

@login_required
def users(request):
    all_users = User.objects.all()
    return render(request, "users.html", context={'title':"Users", 'users': all_users})

@login_required
def logoutView(request):
    logout(request)
    return redirect(loginView)

