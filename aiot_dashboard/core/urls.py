from django.conf.urls import include, url, patterns
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(pattern_name='dashboard_home'), name='frontpage'),
    url(r'^dashboard/', include('aiot_dashboard.apps.dashboard.urls')),
    url(r'^display/', include('aiot_dashboard.apps.display.urls')),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve', kwargs={'insecure': True}),
    )
