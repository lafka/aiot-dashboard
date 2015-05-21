from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='dashboard_home'),
    url(r'^updates/$', views.UpdateSseView.as_view(), name='dashboard_updates'),
    url(r'^rooms/$', views.RoomOverviewView.as_view(), name='dashboard_room_overview'),
    url(r'^rooms/state/$', views.room_overview_state, name='dashboard_room_overview_state'),
    url(r'^rooms/(?P<room_id>\d+)/$', views.RoomView.as_view(), name='dashboard_room')
]
