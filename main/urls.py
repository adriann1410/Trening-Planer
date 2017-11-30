from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.loginView, name="login"),
    url(r'^logout$', views.logoutView, name="logout"),
    url(r'^users$', views.users, name="users"),
    url(r'^coaches$', views.coachesList, name = "coaches"),
    url(r'^rate_coach/$', views.rate_coach, name="rate_coach"),
    url(r'^register$', views.registerView, name="register"),
    url(r'^user/([0-9]+)/$', views.userProfile, name="userProfile")

]