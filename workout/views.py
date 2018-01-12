from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import ScheduleForm, ScheduleEditForm
from .models import Schedule, Workout, Exercise, Plan, Calendar

@login_required
def my_workout(request):
    workouts = Workout.objects.filter(author=request.user).all()
    return render(request, 'my_workout.html', {'workouts': workouts})

@login_required
def workout_detail(request, pk):
    """
        pk - workout.id
    """
    schedules = Workout.schedules.get_all_for(id=pk)
    return render(request, 'workout_detail.html', {"schedules": schedules, 'workout_pk': pk})

@login_required
def calendar(request):
    _calendar = Calendar.get_calendar(request.user)
    return render(request, 'calendar.html', {'calendar' : _calendar})

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
    if workout.author.id not in [request.user.id]:
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

