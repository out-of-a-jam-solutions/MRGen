from django.db import models


class Customer(models.Model):
    name = models.TextField()
    watchman_group_id = models.TextField(unique=True, null=True)
    repairshopr_id = models.TextField(unique=True, null=True)


class WatchmanComputer(models.Model):
    watchman_group_id = models.ForeignKey(Customer,
                                          to_field='watchman_group_id',
                                          db_column='watchman_group_id',
                                          on_delete=models.CASCADE)
    computer_id = models.TextField(unique=True)
    date_reported = models.DateField(auto_now_add=True)
    date_last_reported = models.DateField(auto_now_add=True)
    name = models.TextField()
    os_type = models.CharField(max_length=7)
    os_version = models.TextField()
    ram_gb = models.FloatField()
    hdd_capacity_gb = models.FloatField()
    hdd_usage_gb = models.FloatField()


class WatchmanWarning(models.Model):
    watchman_group_id = models.ForeignKey(Customer,
                                          to_field='watchman_group_id',
                                          db_column='watchman_group_id',
                                          on_delete=models.CASCADE)
    computer_id = models.ForeignKey(WatchmanComputer,
                                    to_field='computer_id',
                                    db_column='computer_id',
                                    on_delete=models.CASCADE)
    warning_id = models.TextField()
    date_reported = models.DateField(auto_now_add=True)
    date_last_checked = models.DateField(auto_now_add=True)
    date_resolved = models.DateField(null=True)
    name = models.TextField()
    details = models.TextField()


class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    date_generated = models.DateField(auto_now_add=True)
    num_current_warnings = models.IntegerField(default=0)
    num_resolved_warnings = models.IntegerField(default=0)
    num_mac_os = models.IntegerField(default=0)
    num_windows_os = models.IntegerField(default=0)
    num_linux_os = models.IntegerField(default=0)
