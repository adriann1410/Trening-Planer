from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from main.models import User


class CoachProfileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_user_coaches(self, user_id):
        query = CoachProfile.objects.filter(pupils__id__contains=user_id).all()
        return query


class CoachProfile(models.Model):
    pupils = models.ManyToManyField(User, related_name='my_coaches')
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='coach_profile')
    description = models.TextField(max_length=500)

    objects = CoachProfileManager()

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    coach = models.ForeignKey(CoachProfile, related_name='comments', verbose_name=("Coach"), default=None, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='sent_comment', verbose_name=("author"), on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=500)
    commentRate = models.DecimalField(max_digits=2, decimal_places=1,
                                      validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return str(self.id)


class CoachApplication(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=500, null=True)
    state = models.BooleanField(default=False, verbose_name="Accept")

    def __str__(self):
        return str(self.sender.email)



