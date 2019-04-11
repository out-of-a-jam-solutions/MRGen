# sheldon woodward
# jan 13, 2019

from django.conf.urls import url
from reporter import views


urlpatterns = [
    url(r'^forward$', views.Forward.as_view(), name='forward'),
    url(r'^customer', views.CustomerLCView.as_view(), name='customer-lc')
]
