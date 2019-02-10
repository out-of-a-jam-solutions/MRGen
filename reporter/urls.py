# sheldon woodward
# jan 13, 2019

from django.conf.urls import url
from reporter import views


urlpatterns = [
    url(r'^computer$', views.Forward.as_view(), name='forward'),
]
