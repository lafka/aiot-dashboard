from django.conf.urls import url

from . import views

urlpatterns = [
    # dashboard home
    url(r'^$', views.DashboardView.as_view(), name='dashboard_home'),
    url(r'^updates/$', views.UpdateSseView.as_view(), name='dashboard_updates'),
    # room overview
    url(r'^rooms/$', views.RoomOverviewView.as_view(), name='dashboard_room_overview'),
    url(r'^rooms/state/$', views.room_overview_state, name='dashboard_room_overview_state'),
    # room vivew
    url(r'^rooms/(?P<room_id>\d+)/$', views.RoomView.as_view(), name='dashboard_room'),
    url(r'^rooms/(?P<room_id>\d+)/state/$', views.room_state, name='dashboard_room_state'),
    # power meters overview
    url(r'^power-meters/$', views.PowerMeterOverviewView.as_view(), name='dashboard_power_meter_overview'),
    url(r'^power-meters/state/$', views.power_meter_overview_state, name='dashboard_power_meter_overview_state'),
]
