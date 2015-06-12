from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^$', views.OperationsView.as_view(), name='operations'),
)
