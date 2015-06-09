from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.DisplayView.as_view(), name='display'),
    url(r'^update/$', views.DataSseView.as_view(), name='display_data_update'),
)
