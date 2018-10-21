from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from coach.models import CoachProfile

BODY_PARTS = (
    ('legs','Legs'),
    ('arms','Arms'),
    ('chest','Chest'),
    ('core','Core'),
    ('back','Back'),
)

PLAN_REPEATS = (
    ('d', "Daily"),
    ('w', 'Weekly'),
    ('m', 'Monthly')
)

class WorkoutScheduleManager(models.Manager):
    def get_all_for(self, id=None):
        if not id:
            id = self.model.pk
        return Schedule.objects.filter(workout_id=id).all()


class WorkoutManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Exercise(models.Model):
    '''
        Pojedyńcze ćwiczenie
    '''
    name = models.CharField(max_length=200)
    body_parts = models.CharField(max_length=200, choices=BODY_PARTS)
    description = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name)


class Workout(models.Model):
    '''
        Trening tj. rozkłady ćwiczeń, autor, trener, data
    '''
    name = models.CharField(max_length=200, default="New workout")
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='my_workouts')
    coach = models.ForeignKey(CoachProfile, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    objects = WorkoutManager()
    schedules = WorkoutScheduleManager()

    @classmethod
    def remove_workout(cls, author, pk):
        workout = get_object_or_404(cls, author=author, id=pk)
        try:
            workout.delete()
        except Exception:
            raise Http404

    def __str__(self):
        return str(self.name)


class Schedule(models.Model):
    '''
        Tzw. Rozkład tj. ćwiczenie; ilość powtórzeń; obciążenie
    '''
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
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
    schedule = models.OneToOneField(Schedule, related_name='performance', on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Calendar(models.Model):
    '''
        Kalendarz treningów
    '''
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @classmethod
    def get_calendar(cls, owner):
        calendar, created = cls.objects.get_or_create(
            owner=owner
        )
        return calendar

    def __str__(self):
        return str(self.id)

#
class Plan(models.Model):
    owner = models.ForeignKey(User, related_name='workout_plans', default=None, on_delete=models.CASCADE)
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, null=True, on_delete=models.CASCADE)
    # calendar = models.ForeignKey(Calendar, related_name='plans')
    date_on = models.DateField(null=True)
    repeats = models.CharField(max_length=10, choices=PLAN_REPEATS, null=True)

    def __str__(self):
        return str(self.id)
#
