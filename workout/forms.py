from django import forms

from .models import Workout, Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['exercise', 'series', 'reps', 'weight']

