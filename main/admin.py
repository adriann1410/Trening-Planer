from django.contrib import admin
from .models import CoachProfile, NormalProfile, Comment
# Register your models here.

admin.site.register(CoachProfile)
admin.site.register(NormalProfile)
admin.site.register(Comment)