from django import template

from social.models import Friend, Message, Invite
from django.contrib.auth.models import User

register = template.Library()


"""
    Main
"""


@register.inclusion_tag("tags_templates/horizontal_form.html")
def horizontal_form(fields):
    return {'fields': fields}

@register.inclusion_tag("tags_templates/profile_navbar.html", takes_context=True)
def profile_navbar(context, current_page, user_id):
    return {'request': context['request'], 'current': current_page, 'user_id': user_id}

"""
    Social
"""

@register.assignment_tag(takes_context=True)
def isFriend(context, user_id):
    user = User.objects.get(id=user_id)
    if user == context['request'].user:
        return False
    return user in Friend.list.for_user(context['request'].user)

@register.simple_tag(takes_context=True)
def conversationReceiver(context, conversation):
    receiver = conversation.members.all().exclude(email=context['request'].user.email).first()
    return receiver

@register.assignment_tag(takes_context=True)
def unreadMessages(context):
    _user = context['request'].user
    new_messages = Message.list.for_user(_user).filter(read=False).exclude(author__email=_user.email).count()
    return new_messages

@register.assignment_tag(takes_context=True)
def getNewInvites(context):
    new_invites = Invite.pending.for_user(context['request'].user).count()
    return new_invites

"""
    Workout
"""

@register.inclusion_tag("tags_templates/workout_navbar.html", takes_context=True)
def workout_navbar(context):
    return {'request':context['request']}

@register.assignment_tag()
def mark2delete(workout_id):
    return workout_id

