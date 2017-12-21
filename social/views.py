from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message, Conversation, Friend, Invite
from .forms import MessageForm

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user)
    messages = Message.list.for_user(request.user)
    return render(request, 'inbox.html', {'conversations': messages})

@login_required
def new_message(request, pk):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        receiver = User.objects.get(id=pk)
        if form.is_valid() and receiver:
            new_mess = form.save(commit=False)
            new_mess.author = request.user
            new_mess.receiver = receiver
            new_mess.save()
            return redirect(to=inbox)
    else:
        form = MessageForm()
        return render(request, 'new_message.html', {'form': form})

@login_required
def friends_list(request):
    pending = Invite.pending.for_user(request.user)
    friends = Friend.list.for_user(request.user)
    return render(request, 'friends.html', {'friends': friends, 'pending': pending})

@login_required
def add_friend(request, pk):

    if pk == request.user.id:
        return redirect(to=friends_list)

    if User.objects.get(id=pk) in Friend.list.for_user(request.user):
        return redirect(to=friends_list)

    user_to_invite = User.objects.get(id=pk)
    Invite(sender=request.user, receiver=user_to_invite).save()

    return redirect(to=friends_list)

@login_required
def accept_invite(request, pk):
    invite = Invite.pending.for_user(request.user).get(id=pk)
    if invite:
        invite.accepted = 'a'
        invite.save()

    return redirect(to=friends_list)

@login_required
def decline_invite(request, pk):
    invite = Invite.pending.for_user(request.user).get(id=pk)
    if invite:
        invite.accepted = 'r'
        invite.save()

    return redirect(to=friends_list)
