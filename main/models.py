from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    rate = models.FloatField(default=0)
    rate_sum = models.IntegerField(default=0)
    rate_counter = models.IntegerField(default=0)
    img_url = models.CharField(max_length=250, default="./static/img/default_user.png") #do zmiany przy uploadowaniu wlasnych plikow

    def __str__(self):
        return self.user.username


class NormalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Pupil(models.Model):
    coach_id = models.ForeignKey(CoachProfile)
    pupil_id = models.OneToOneField(NormalProfile)

    def __str__(self):
        return self.id


class Training(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercises_num = models.IntegerField(default=0)
    b_weight = models.IntegerField(default=0)

    def __str__(self):
        return self.id


class Exercise(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    series = models.IntegerField(default=0)
    reps = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.exercise_name


class Message(models.Model):
    author = models.ForeignKey(User, related_name='sent_messages', verbose_name=("Sender"))
    receiver = models.ForeignKey(User, related_name='received_messages', verbose_name=("Reveiver"))
    content = models.TextField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.id

