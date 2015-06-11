from django.conf.urls import url

from . import views

urlpatterns = [
    # room overview
    url(r'^$', views.RoomOverviewView.as_view(), name='room_overview'),
    url(r'^events/$', views.RoomOverviewEventsView.as_view(), name='room_overview_events'),

    # room detail
    url(r'^(?P<room_key>\d+)/$', views.RoomDetailView.as_view(), name='room_detail'),
    url(r'^(?P<room_key>\d+)/events/$', views.RoomDetailEventsView.as_view(), name='room_detail_events'),
]
