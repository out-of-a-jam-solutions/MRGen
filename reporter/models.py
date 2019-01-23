from django.db import models


class Customer(models.Model):
    watchman_id = models.TextField()
    repairshopr_id = models.TextField()


class WatchmanWarning(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    computer_id = models.TextField()
    warning_id = models.TextField()
    date_reported = models.DateField()
    date_resolved = models.DateField()
