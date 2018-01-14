from django.shortcuts import render, redirect
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Comment, CoachProfile, CoachApplication
from .forms import UpgradeProfileForm
from main.models import Profile
from workout.views import my_workout

@login_required
def coach_panel(request):
    return render(request, 'coach_panel.html', {'pupils': None})

@login_required
def start_collaboration(request, pk):
    # pk - coach pk
    if request.user.id == pk:
        return redirect(to=coachesList)

    coach = CoachProfile.objects.filter(user__id=pk).first()
    if coach:
        coach.pupils.add(request.user)

    return redirect(to=my_workout)


def coachesList(request):
    avg_rates = {}
    coaches = CoachProfile.objects.all().exclude(user=request.user)
    for coach in coaches:
        average_rate = Comment.objects.filter(coach_id=coach.id).aggregate(Avg('commentRate'))
        avg_rates[coach.user.id] = average_rate['commentRate__avg']


    return render(request, "coaches.html", {'coaches': coaches, 'avg_rates': avg_rates})


@login_required
def createCoachProfile(request):
    profile = Profile.objects.filter(user=request.user).first()
    if profile.isCoach:
        error = "Your account is already Coach Account"
        return render(request, 'become_coach.html', {'error': error})

    user_app = CoachApplication.objects.filter(sender__id=request.user.id).first()
    if user_app:
        error = "You already send application"
        return render(request, 'become_coach.html', {'error': error})

    if request.method == 'POST':
        form = UpgradeProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_app = CoachApplication(sender=request.user, note=cd.get('note'))
            new_app.save()
            message = "Application was send ! We will contact you soon"
            return render(request, 'become_coach.html', {'message': message})
    else:
        form = UpgradeProfileForm()
    return render(request, 'become_coach.html', {'form': form})


