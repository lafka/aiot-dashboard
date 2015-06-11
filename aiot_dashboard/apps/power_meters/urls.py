from django.conf.urls import url

from . import views

urlpatterns = [
    # overview
    url(r'^$', views.PowerMetersOverviewView.as_view(), name='power_meters_overview'),
    url(r'^state/$', views.PowerMetersOverviewEventsView.as_view(), name='power_meters_overview_events'),

    # detail
    url(r'^(?P<power_circuit_id>\d+)/$', views.PowerMetersDetailView.as_view(), name='power_meters_detail'),
    url(r'^(?P<power_circuit_id>\d+)/events/$', views.PowerMetersDetailEventsSseView.as_view(), name='power_meters_detail_events'),
]
