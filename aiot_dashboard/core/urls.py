from django.conf.urls import include, url, patterns
from django.conf import settings

from aiot_dashboard.apps.dashboard.views import DashboardView

urlpatterns = [
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$', DashboardView.as_view(), name='dashboard_home'),
    url(r'^dash/', include('aiot_dashboard.apps.dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve', kwargs={'insecure': True}),
    )
