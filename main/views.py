from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import  settings

from .forms import LoginForm, UserForm, UserUpdateForm, ProfileUpdateForm, CommentForm, ProfileImageForm
from coach.models import Comment

from social.models import Friend



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect(to=userProfile, pk=request.user.id) # reverse
    return render(request, "index.html", context={'title':"Index"})


def userProfile(request, pk):

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = Comment(
                                coach=User.objects.get(id=pk).coachprofile,
                                author=request.user,
                                content=form.cleaned_data.get("content"),
                                commentRate= form.cleaned_data.get("commentRate")
                                )
            new_comment.save()
        return redirect('./')
    else:
        user = User.objects.get(id=pk)

        if not user:
            return redirect(to=pageNotFound)

        profile = user.profile

        if profile.isCoach:
                form = CommentForm()
                coach = user.coachprofile
                comments = reversed(coach.comments.all())
                return render(request, 'coachProfile.html', {'coach': coach, 'comments': comments, 'form': form})
        else:
            return render(request, "userProfile.html", {'page_user': profile})


@login_required
def userProfileEdit(request):
    current_user = request.user
    user_profile = current_user.profile

    if request.method == 'POST':
        profile_update = ProfileUpdateForm(request.POST, instance=user_profile)
        profile_image_form = ProfileImageForm(data=request.POST, files=request.FILES, instance=user_profile)
        user_update = UserUpdateForm(request.POST, instance=current_user)


        if user_update.is_valid():
            user_update.save(user_id=request.user.id)

        if profile_image_form.is_valid():
            profile_image_form.save(user_id=request.user.id)

        if profile_update.is_valid():
            profile_update.save(user_id=request.user.id)

        return redirect(to=userProfileEdit)

    update_profile_form = ProfileUpdateForm()
    update_user_form = UserUpdateForm()
    profile_image_form = ProfileImageForm()

    return render(request, "profile_edit.html", {'image_form': profile_image_form, 'profile_form': update_profile_form, 'user_form': update_user_form, 'user': current_user, 'user_profile': user_profile})


def loginView(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.get(email=email)

            if not user.check_password(password):
                message = "Password is not correct"
                message_type = "success"
                return render(request, "login.html", context={'title':"Login", 'form': form, 'message': message, 'message_type': message_type})

            login(request, user)
            return redirect(index)
    else:
        form = LoginForm()

    return render(request, "login.html", context={'title':"Login", 'form': form})


def registerView(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(email=cd.get('email'))
                if user:
                    message = "Email already in use xd"
                    message_type = "danger"
                    return render(request, "register.html", context={'title': "Register", 'form': form, 'message':message, 'message_type': message_type})
            except User.DoesNotExist as e:
                pass
            password = make_password(cd.get('password'))

            new_user = User(email=cd.get('email'), password=password, username=cd.get('email'))
            new_user.save()
            Friend(current_user=new_user).save()


            subject = "Dziękujemy za rejestrację w Planer"
            mail_message = "Tutaj bedzie link do potwierdzenia konta"
            # socket.getaddrinfo('127.0.0.1', 8000)
            try:
                send_mail(subject, mail_message, settings.EMAIL_HOST_USER, [cd.get('email')], fail_silently=True)
            except Exception as e:
                pass
            else:
                message = "Confirmation mail has been send, you can now login"
                message_type = "success"
                return render(request, "register.html", context={'title': "Register", 'form': form, 'message': message, 'message_type': message_type})
    else:
        form = UserForm
    return render(request, "register.html", context={'title':"Register", 'form': form})


def pageNotFound(request):
    return render(request, '404.html')

@login_required
def users(request):
    all_users = User.objects.all().exclude(id=request.user.id)
    return render(request, "users.html", context={'title':"Users", 'users': all_users})

@login_required
def logoutView(request):
    logout(request)
    return redirect(loginView)

