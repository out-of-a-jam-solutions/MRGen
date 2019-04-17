# sheldon woodward
# jan 13, 2019

from django.conf.urls import url
from reporter import views


urlpatterns = [
    url(r'^forward$', views.Forward.as_view(), name='forward'),
    url(r'^customer$', views.CustomerLCView.as_view(), name='customer-lc'),
    url(r'^customer/(?P<pk>\d+)$', views.CustomerRUDView.as_view(), name='customer-rud'),
    url(r'^schedule$', views.ScheduleLCView.as_view(), name='schedule-lc'),
    url(r'^schedule/(?P<pk>\d+)$', views.ScheduleRDView.as_view(), name='schedule-rd')
]
