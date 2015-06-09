from django.conf.urls import include, url, patterns
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='dashboard_home'), name='frontpage'),
    url(r'^display/', include('aiot_dashboard.apps.display.urls')),
    url(r'^rooms/', include('aiot_dashboard.apps.rooms.urls')),
    url(r'^power-meters/', include('aiot_dashboard.apps.power_meters.urls')),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve', kwargs={'insecure': True}),
    )
