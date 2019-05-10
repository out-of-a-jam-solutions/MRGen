from django.contrib import admin
from reporter import models

admin.site.register(models.Customer)
admin.site.register(models.ServiceSchedule)
admin.site.register(models.WatchmanComputer)
admin.site.register(models.WatchmanWarning)
admin.site.register(models.Report)
