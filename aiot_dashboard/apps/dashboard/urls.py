from django.conf.urls import url

from . import views

urlpatterns = [
    # dashboard home
    url(r'^$', views.DashboardView.as_view(), name='dashboard_home'),
    url(r'^updates/$', views.UpdateSseView.as_view(), name='dashboard_updates'),
    # room overview
    url(r'^rooms/$', views.RoomOverviewView.as_view(), name='dashboard_room_overview'),
    url(r'^rooms/state/$', views.room_overview_state, name='dashboard_room_overview_state'),
    # room view
    url(r'^rooms/(?P<room_id>\d+)/$', views.RoomView.as_view(), name='dashboard_room'),
    url(r'^rooms/(?P<room_id>\d+)/(?P<limit>\d+)/state/$', views.room_state, name='dashboard_room_state'),
    url(r'^rooms/(?P<room_id>\d+)/state_for_graph/$', views.room_state_for_graph, name='dashboard_room_state_for_graph'),
    # power meters overview
    url(r'^power-meters/$', views.PowerMeterOverviewView.as_view(), name='dashboard_power_meter_overview'),
    url(r'^power-meters/state/$', views.power_meter_overview_state, name='dashboard_power_meter_overview_state'),
    # power meters view
    url(r'^power-meters/(?P<device_key>\w+)/$', views.PowerMeterView.as_view(), name='dashboard_power_meter'),
    url(r'^power-meters/(?P<device_key>\w+)/state/$', views.power_meter_state, name='dashboard_power_meter_state'),
]
