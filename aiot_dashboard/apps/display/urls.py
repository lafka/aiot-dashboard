from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.DisplayView.as_view(), name='display'),
    url(r'^update/stats/$', views.StatsSseView.as_view(), name='display_stats_update')
)
