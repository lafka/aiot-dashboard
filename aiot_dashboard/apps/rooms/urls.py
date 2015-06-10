from django.conf.urls import url

from . import views

urlpatterns = [
    # room overview
    url(r'^$', views.RoomOverviewView.as_view(), name='room_overview'),
    url(r'^updates/$', views.room_overview_state, name='room_overview_state'),

    # room detail
    url(r'^(?P<room_key>\d+)/$', views.RoomView.as_view(), name='room_detail'),
    url(r'^(?P<room_key>\d+)/updates/$', views.RoomEventsSseView.as_view(), name='room_detail_events'),
]
