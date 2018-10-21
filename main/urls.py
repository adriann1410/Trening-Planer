from django.conf.urls import url, include
from django.urls import path, re_path
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.loginView, name="login"),
    url(r'^logout$', views.logoutView, name="logout"),
    url(r'^users$', views.users, name="users"),
    url(r'^register$', views.registerView, name="register"),
    url(r'^user/edit$', views.userProfileEdit, name='editProfile'),
    path('user/<int:pk>/', views.userProfile, name="userProfile")
]