from django.db import models
from django.contrib.auth.models import User

from main.models import CoachProfile

BODY_PARTS = (
    ('legs','Legs'),
    ('arms','Arms'),
    ('chest','Chest'),
    ('core','Core'),
    ('back','Back'),
)

class Exercise(models.Model):
    '''
        Pojedyńcze ćwiczenie
    '''
    name = models.CharField(max_length=200)
    body_parts = models.CharField(max_length=200, choices=BODY_PARTS)
    description = models.CharField(max_length=250)

    def __str__(self):
        return str(self.id)


class Workout(models.Model):
    '''
        Trening tj. rozkłady ćwiczeń, autor, trener, data
    '''
    name = models.CharField(max_length=200, default="New workout")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(CoachProfile, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Schedule(models.Model):
    '''
        Tzw. Rozkład tj. ćwiczenie; ilość powtórzeń; obciążenie
    '''
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='plan')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    series = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Performance(models.Model):
    '''
        Archiwizacja wykonanych ćwiczeń
    '''
    schedule = models.OneToOneField(Schedule, related_name='performance')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Calendar(models.Model):
    '''
        Kalendarz treningów
    '''
    pass
