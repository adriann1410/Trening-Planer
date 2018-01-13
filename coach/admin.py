from django.contrib import admin
from .models import CoachApplication
from main.models import Profile
from .models import CoachProfile

class CoachApplicationAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'note', 'date',)
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            if obj.state:
                profile = Profile.objects.filter(user=obj.sender).first()
                profile.isCoach = True
                profile.save()
                new_coachProfile = CoachProfile(user=obj.sender)
                new_coachProfile.save()
            obj.delete()


admin.site.register(CoachApplication, CoachApplicationAdmin)

# Register your models here.
