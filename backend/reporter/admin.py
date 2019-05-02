from django.contrib import admin
from backend.reporter import models

admin.site.register(models.Customer)
admin.site.register(models.WatchmanComputer)
admin.site.register(models.WatchmanWarning)
admin.site.register(models.Report)
