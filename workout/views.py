from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ScheduleForm
from .models import Schedule, Workout, Exercise, Plan, Calendar
from coach.models import CoachProfile

import datetime


@login_required
def my_workout(request):
    workouts = Workout.objects.filter(author=request.user).all()
    coachProfile = CoachProfile.objects.filter(user=request.user).first()
    if coachProfile:
        my_pupils = coachProfile.pupils.all()
        return render(request, 'my_workout.html', {'workouts': workouts,
                                                   'my_pupils': my_pupils})

    return render(request, 'my_workout.html', {'workouts': workouts})

@login_required
def workout_detail(request, pk):
    """
        pk - workout.id
    """
    schedules = Workout.schedules.get_all_for(id=pk)
    if request.method == 'POST':
        _date = request.POST['plan-date']

        workout = Workout.objects.filter(id=pk).first()
        if _date and workout:
            new_plan = Plan(owner=request.user,
                            author=request.user,
                            workout=workout,
                            date_on=_date)
            new_plan.save()
            message = "New plan created"
            mode = "success"
            return render(request, 'workout_detail.html', {"schedules": schedules,
                                                           'workout_pk': pk,
                                                           'message': message,
                                                           'mode': mode})
        message = "Please select the date"
        mode = "danger"
        return render(request, 'workout_detail.html', {"schedules": schedules,
                                                       'workout_pk': pk,
                                                       'message': message,
                                                       'mode': mode})

    return render(request, 'workout_detail.html', {"schedules": schedules, 'workout_pk': pk})

@login_required
def calendar(request):
    _calendar = Calendar.get_calendar(request.user)

    if request.method == 'POST':
        date = request.POST['calendar-date']
        if date:
            month, year = date.split('/')
            return render(request, 'calendar.html', {'calendar': _calendar,
                                                     'month': month,
                                                     'year': year})
    today = datetime.date.today()
    return render(request, 'calendar.html', {'calendar' : _calendar,
                                             'month': today.month,
                                             'year': today.year})


@login_required
def create_plan(request, pk):
    if request.method == 'POST':

        pass

    return render(request, "planworkout.html")

@login_required
def add_workout(request):

    if request.method == 'POST':
        workoutName = request.POST['workoutName']
        exerciseInput = request.POST.getlist('exerciseInputs[]')
        seriesInput = request.POST.getlist('seriesInputs[]')
        repsInput = request.POST.getlist('repsInputs[]')
        weightInput = request.POST.getlist('weightInputs[]')

        new_workout = Workout(name=workoutName, author=request.user)
        new_workout.save()

        for i in range(len(exerciseInput)):
            exercise = Exercise.objects.get(name__exact=exerciseInput[i])
            new_schedule = Schedule(workout=new_workout,
                                    exercise=exercise,
                                    series=seriesInput[i],
                                    reps=repsInput[i],
                                    weight=weightInput[i])
            new_schedule.save()

        return redirect(to=my_workout)


    exercises = Exercise.objects.all()
    form = ScheduleForm()
    return render(request, 'add_workout.html', {'form':form, 'exercises': exercises})

@login_required
def edit_workout(request, pk):
    workout = get_object_or_404(Workout, id=pk)
    schedules = Workout.schedules.get_all_for(id=pk)
    white_list = CoachProfile.objects.get_user_coaches(workout.author.id)
    white_list = [x.user_id for x in white_list]
    white_list.append(workout.author.id)

    if request.user.id not in white_list:
        message = "You have no permissions to edit this workout"
        return render(request, 'workout_error.html', {'message': message})

    if request.method == 'POST':
        seriesInput = request.POST.getlist('seriesInputs[]')
        repsInput = request.POST.getlist('repsInputs[]')
        weightInput = request.POST.getlist('weightInputs[]')


        for i in range(len(schedules)):
            if seriesInput[i] is not '':
                schedules[i].series = seriesInput[i]
            if repsInput[i] is not '':
                schedules[i].reps = repsInput[i]
            if weightInput[i] is not '':
                schedules[i].weight = weightInput[i]
            schedules[i].save()


        return redirect(to=workout_detail, pk=pk)

    return render(request, 'edit_workout.html', {'schedules': schedules, 'workout_pk': pk})


@login_required
def delete_workout(request, pk):
    Workout.remove_workout(request.user, pk)
    return redirect(to=my_workout)

