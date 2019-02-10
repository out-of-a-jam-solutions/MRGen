from django.db import models


class Customer(models.Model):
    name = models.TextField()
    watchman_group_id = models.TextField(unique=True, null=True)
    repairshopr_id = models.TextField(unique=True, null=True)


class WatchmanWarning(models.Model):
    watchman_group_id = models.ForeignKey(Customer,
                                          to_field='watchman_group_id',
                                          db_column='watchman_group_id',
                                          on_delete=models.CASCADE)
    computer_id = models.TextField()
    warning_id = models.TextField()
    date_reported = models.DateField(auto_now_add=True)
    date_last_checked = models.DateField(auto_now_add=True)
    date_resolved = models.DateField(null=True)
    name = models.TextField()
    details = models.TextField()
