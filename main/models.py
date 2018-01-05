from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isCoach = models.BooleanField(default=False)
    old = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_image', blank=True)


    def __str__(self):
        return self.user.username


class CoachProfile(models.Model):
    # pupils = models.OneToManyField(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    coach = models.ForeignKey(CoachProfile, related_name='comments', verbose_name=("Coach"), default=None)
    author = models.ForeignKey(User, related_name='sent_comment', verbose_name=("author"))
    date = models.DateField(default=datetime.date.today)
    content = models.TextField(max_length=500)
    commentRate = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return str(self.id)


class Pupil(models.Model):
    coach_id = models.ForeignKey(CoachProfile)
    pupil_id = models.OneToOneField(Profile)

    def __str__(self):
        return self.id


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
