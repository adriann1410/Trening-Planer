from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from main.models import User


class CoachProfile(models.Model):
    pupils = models.ManyToManyField(User, related_name='my_coach')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    coach = models.ForeignKey(CoachProfile, related_name='comments', verbose_name=("Coach"), default=None)
    author = models.ForeignKey(User, related_name='sent_comment', verbose_name=("author"))
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=500)
    commentRate = models.DecimalField(max_digits=2, decimal_places=1,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return str(self.id)
