from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.loginView, name="login"),
    url(r'^logout$', views.logoutView, name="logout"),
    url(r'^register$', views.registerView, name="register"),
    url(r'^users$', views.users, name="users")
]