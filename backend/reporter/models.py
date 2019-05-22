from django.db import models
from django_celery_beat.models import PeriodicTask


class Customer(models.Model):
    name = models.CharField(max_length=100)
    watchman_group_id = models.CharField(max_length=100, unique=True, null=True)
    repairshopr_id = models.CharField(max_length=100, unique=True, null=True)

    class Meta:
        ordering = ['id']


class ServiceSchedule(models.Model):
    customer = models.ForeignKey(Customer,
                                 db_column='customer_id',
                                 on_delete=models.CASCADE)
    periodic_task = models.OneToOneField(PeriodicTask,
                                         db_column='periodic_task_id',
                                         on_delete=models.CASCADE)
    task_type = models.CharField(max_length=25)

    class Meta:
        ordering = ['id']

class Computer(models.Model):
    name = models.CharField(max_length=100)
    os_type = models.CharField(max_length=7)
    os_version = models.CharField(max_length=100)
    ram_gb = models.FloatField()
    hdd_capacity_gb = models.FloatField()
    hdd_usage_gb = models.FloatField()

    class Meta:
        abstract = True


class WatchmanComputer(Computer):
    watchman_group_id = models.ForeignKey(Customer,
                                          to_field='watchman_group_id',
                                          db_column='watchman_group_id',
                                          on_delete=models.CASCADE)
    computer_id = models.CharField(max_length=100, unique=True)
    date_reported = models.DateField(auto_now_add=True)
    date_last_reported = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']


class WatchmanWarning(models.Model):
    watchman_group_id = models.ForeignKey(Customer,
                                          to_field='watchman_group_id',
                                          db_column='watchman_group_id',
                                          on_delete=models.CASCADE)
    computer_id = models.ForeignKey(WatchmanComputer,
                                    to_field='computer_id',
                                    db_column='computer_id',
                                    on_delete=models.CASCADE)
    warning_id = models.CharField(max_length=100)
    date_reported = models.DateField(auto_now_add=True)
    date_last_checked = models.DateField(auto_now_add=True)
    date_resolved = models.DateField(null=True)
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']


class Report(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    date_generated = models.DateField(auto_now_add=True)
    num_mac_os = models.IntegerField(default=0)
    num_windows_os = models.IntegerField(default=0)
    num_linux_os = models.IntegerField(default=0)

    class Meta:
        ordering = ['id']

class SubReport(models.Model):
    report = models.ForeignKey(Report, db_column='report_id', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    num_warnings_unresolved_start = models.IntegerField(default=0)
    num_warnings_unresolved_end = models.IntegerField(default=0)
    num_warnings_created = models.IntegerField(default=0)
    num_warnings_resolved = models.IntegerField(default=0)
    num_tickets_created = models.IntegerField(default=0)
    num_tickets_resolved = models.IntegerField(default=0)

    class Meta:
        ordering = ['start_date']

class ComputerReport(Computer):
    computer = models.OneToOneField(WatchmanComputer, null=True, db_column='computer_id', on_delete=models.SET_NULL)
