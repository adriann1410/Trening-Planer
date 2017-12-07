from django.contrib import admin
from .models import CoachProfile, Profile, Comment
# Register your models here.

admin.site.register(CoachProfile)
admin.site.register(Profile)
admin.site.register(Comment)