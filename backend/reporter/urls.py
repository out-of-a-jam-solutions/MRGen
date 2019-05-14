# sheldon woodward
# jan 13, 2019

from django.conf.urls import url
from reporter import views


urlpatterns = [
    url(r'^forward$', views.Forward.as_view(), name='forward'),
    url(r'^customer$', views.CustomerLCView.as_view(), name='customer-lc'),
    url(r'^customer/(?P<pk>\d+)$', views.CustomerRDView.as_view(), name='customer-rd'),
    url(r'^schedule$', views.ScheduleLCView.as_view(), name='schedule-lc'),
    url(r'^schedule/(?P<pk>\d+)$', views.ScheduleRDView.as_view(), name='schedule-rd'),
    url(r'^report$', views.ReportLCView.as_view(), name='report-lc')
]
