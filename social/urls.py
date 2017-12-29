from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.inbox),
    url(r'messages/all$', views.inbox, name='inbox'),
    url(r'friends$', views.friends_list, name='friends_list'),
    url(r'conversation/(?P<pk>[0-9]+)/$', views.conversation, name='conversation'),
    url(r'friends/add/(?P<pk>[0-9]+)/$', views.add_friend, name='friend_add'),
    url(r'message/new/(?P<pk>[0-9]+)/$', views.new_message, name='new_message'),
    url(r'invite/accept/(?P<pk>[0-9]+)/$', views.accept_invite, name='accept_invite'),
    url(r'invite/decline/(?P<pk>[0-9]+)/$', views.decline_invite, name='decline_invite')
]