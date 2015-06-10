from django.conf.urls import url

from . import views

urlpatterns = [
    # overview
    url(r'^$', views.PowerMetersOverviewView.as_view(), name='power_meters_overview'),
    url(r'^state/$', views.power_meters_overview_state, name='power_meters_overview_state'),

    # detail
    url(r'^(?P<room_id>\d+)/$', views.PowerMetersDetailView.as_view(), name='power_meters_detail'),
    url(r'^(?P<room_id>\d+)/events/$', views.power_meters_detail_state, name='power_meters_detail_state'),
]
