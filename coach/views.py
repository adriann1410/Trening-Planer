from django.shortcuts import render
from django.db.models import Avg
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Comment, CoachProfile


@login_required
def coach_panel(request):
    return render(request, 'coach_panel.html', {'pupils': None})


def coachesList(request):
    avg_rates = {}
    coaches = CoachProfile.objects.all()
    for coach in coaches:
        average_rate = Comment.objects.filter(coach_id=coach.id).aggregate(Avg('commentRate'))
        avg_rates[coach.user.id] = average_rate['commentRate__avg']


    return render(request, "coaches.html", {'coaches': coaches, 'avg_rates': avg_rates})


@login_required
def createCoachProfile(request):
    return render(request, 'become_coach.html')


