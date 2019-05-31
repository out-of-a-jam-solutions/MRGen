# sheldon woodward
# jan 13, 2019

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from reporter import views


urlpatterns = [
    url(r'^forward$', views.Forward.as_view(), name='forward'),
    url(r'^customer$', views.CustomerLCView.as_view(), name='customer-lc'),
    url(r'^customer/(?P<pk>\d+)$', views.CustomerRDView.as_view(), name='customer-rd'),
    url(r'^schedule$', views.ScheduleLCView.as_view(), name='schedule-lc'),
    url(r'^schedule/(?P<pk>\d+)$', views.ScheduleRDView.as_view(), name='schedule-rd'),
    url(r'^report$', views.ReportLCView.as_view(), name='report-lc'),
    url(r'^report/(?P<pk>\d+)$', views.ReportDeleteView.as_view(), name='report-d'),
    url(r'^report/detail/(?P<pk>\d+).pdf$', views.ReportPDFView.as_view(), name='report-pdf')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
