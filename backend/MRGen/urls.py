import os

from django.contrib import admin
from django.urls import include, re_path


urlpatterns = [
    re_path(r'^{}'.format(os.getenv('DJANGO_BASE_URI', '')), include([
        re_path(r'^admin/', admin.site.urls),
        re_path(r'^auth/', include('knox.urls')),
        re_path(r'^api/', include(('reporter.urls', 'reporter'), namespace='reporter')),
    ]))
]
