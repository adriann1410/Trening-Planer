from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.my_workout, name='my_workout'),
    url(r'^calendar$', views.calendar, name='calendar'),
    url(r'^add$', views.add_workout, name='add_workout'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.workout_detail, name='workout_detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_workout, name='delete_workout'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit_workout, name='edit_workout')
]