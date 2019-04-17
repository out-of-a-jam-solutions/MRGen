from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import serializers, status

from reporter import models


class PeriodicTaskField(serializers.Field):
    def get_value(self, dictionary):
        # s = super(PeriodicTaskField, self).get_value(dictionary)
        return dictionary

    def to_representation(self, obj):
        return {
            'minute': obj.crontab.minute,
            'hour': obj.crontab.hour,
            'day_of_week': obj.crontab.day_of_week,
            'day_of_month': obj.crontab.day_of_month,
            'month_of_year': obj.crontab.month_of_year
        }

    def to_internal_value(self, data):
        # retrieve the customer or raise validation error if customer does not exist
        try:
            customer = models.Customer.objects.get(pk=data['customer'])
        except KeyError:
            raise serializers.ValidationError({'customer': 'This field is required'}, status.HTTP_400_BAD_REQUEST)
        except models.Customer.DoesNotExist:
            raise serializers.ValidationError({'customer': 'This field must be a valid customer id'}, status.HTTP_404_NOT_FOUND)
        # create the task name
        task_name = '{} {}'.format(customer.name, data['task_type'])
        # get or create the cron schedule
        cron, _ = CrontabSchedule.objects.get_or_create(**data['periodic_task'])
        # check if a periodic task with the same name already exists
        if PeriodicTask.objects.filter(name=task_name).exists():
            raise serializers.ValidationError('A periodic task with this name already exists')
        # choose the task name
        if data['task_type'] == 'watchman':
            task_type = 'reporter.tasks_watchman.update_client'
            task_args = [customer.watchman_group_id]
        elif data['task_type'] == 'repairshopr':
            task_type = 'reporter.tasks_repairshopr.update_client'
            task_args = [customer.repairshopr_id]
        # prepare the periodic
        task = PeriodicTask(crontab=cron,
                            name=task_name,
                            task=task_type,
                            args=task_args)
        return task


class ScheduleSerializer(serializers.ModelSerializer):
    periodic_task = PeriodicTaskField()
    task_type = serializers.ChoiceField(('watchman', 'repairshopr'))

    class Meta:
        model = models.Schedule
        fields = (
            'pk',
            'periodic_task',
            'customer',
            'task_type'
        )

    def create(self, validated_data):
        # create the periodic task
        validated_data['periodic_task'].save()
        # call super method
        return super(ScheduleSerializer, self).create(validated_data)
