from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.coach_panel, name="coach_panel"),
    url(r'^list', views.coachesList, name="coaches"),
    url(r'^become_coach', views.createCoachProfile, name="become_coach"),
]