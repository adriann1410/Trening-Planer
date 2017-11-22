from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CoachProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    rate = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


class NormalProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.user.username