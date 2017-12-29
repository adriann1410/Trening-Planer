from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

CHOICES = (
        ('w', "Waiting"),
        ('a', "Accepted"),
        ('r', "Rejected")
    )

class ConversationListManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().filter(models.Q(members__email__icontains=user.email)).all()

    def between(self, user, receiver):
        return super().get_queryset().filter(models.Q(members__email__icontains=user.email)).filter(
                                             models.Q(members__email__icontains=receiver.email)).first()

class MessagesListManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().filter(models.Q(author=user) | models.Q(receiver=user)).all()

class FriendListManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().get(current_user=user).users.all()


class FriendInviteManager(models.Manager):
    def for_user(self, user):
        return super().get_queryset().filter(receiver=user, accepted='w')


class FriendManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Invite(models.Model):
    sender = models.ForeignKey(User, related_name='invites_send')
    receiver = models.ForeignKey(User, related_name='invites_received')
    accepted = models.CharField(max_length=1, choices=CHOICES, default=CHOICES[0][0])

    pending = FriendInviteManager()

    def __str__(self):
        return str(self.id)


class Friend(models.Model):
    users = models.ManyToManyField(User, related_name='friends')
    current_user = models.ForeignKey(User, related_name='friend_object', null=True)

    objects = FriendManager()
    list = FriendListManager()

    @classmethod
    def create_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user,
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user,
        )
        friend.users.remove(new_friend)

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    author = models.ForeignKey(User, related_name='sent_messages', verbose_name=("Sender"))
    receiver = models.ForeignKey(User, related_name='received_messages', verbose_name=("Reveiver"))
    content = models.TextField(max_length=500)
    read = models.BooleanField(default=False)
    send = models.DateTimeField(auto_now_add=True)

    list = MessagesListManager()


    def __str__(self):
        return str(self.id)


class Conversation(models.Model):
    members = models.ManyToManyField(User, related_name='conversations')
    messages = models.ManyToManyField(Message, related_name='messages')

    list = ConversationListManager()

    @classmethod
    def create_conversation(cls, current_user, new_receiver):
        new_conv = Conversation()
        new_conv.save()
        new_conv.members.add(current_user, new_receiver)
        new_conv.save()
        return new_conv

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=Invite)
def create_friend_from_invite(sender, instance, **kwargs):
    if instance.accepted == 'a':
        Friend.create_friend(current_user=instance.receiver, new_friend=instance.sender)
        Friend.create_friend(current_user=instance.sender, new_friend=instance.receiver)

