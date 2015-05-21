from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^updates/$', views.UpdateSseView.as_view(), name='dashboard_updates'),
    url(r'^rooms/$', views.RoomOverviewView.as_view(), name='dashboard_room_overview'),
    url(r'^rooms/(?P<room_id>\d+)/$', views.RoomView.as_view(), name='dashboard_room')
]
