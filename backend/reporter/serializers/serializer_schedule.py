import re

from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import serializers

from reporter import models


class PeriodicTaskField(serializers.Field):
    def get_value(self, dictionary):
        # s = super(PeriodicTaskField, self).get_value(dictionary)
        return dictionary

    def to_representation(self, value):
        return {
            'minute': value.crontab.minute,
            'hour': value.crontab.hour,
            'day_of_week': value.crontab.day_of_week,
            'day_of_month': value.crontab.day_of_month,
            'month_of_year': value.crontab.month_of_year
        }

    def to_internal_value(self, data):
        # retrieve the customer or raise validation error if customer does not exist
        try:
            customer = models.Customer.objects.get(pk=data['customer'])
        except KeyError:
            raise serializers.ValidationError({'customer': 'This field is required'})
        except models.Customer.DoesNotExist:
            raise serializers.ValidationError({'customer': 'This field must be a valid customer id'})
        # create the appropriate task type, either watchman or repairshopr
        if data['task_type'] == 'watchman':
            task_type = 'reporter.tasks_watchman.update_client'
            task_args = [customer.watchman_group_id]
        elif data['task_type'] == 'repairshopr':
            task_type = 'reporter.tasks_repairshopr.update_client'
            task_args = [customer.repairshopr_id]
        else:
            raise serializers.ValidationError({'task_type': 'This field must be either "watchman" or "repairshopr"'})
        # check that the customer has the appropriate service id for the specified task type
        if data['task_type'] == 'watchman' and customer.watchman_group_id is None:
            raise serializers.ValidationError({'task_type': 'The specified customer does not have a Watchman ID defined'})
        if data['task_type'] == 'repairshopr' and customer.repairshopr_id is None:
            raise serializers.ValidationError({'task_type': 'The specified customer does not have a RepairShopr ID defined'})
        # create the task name
        task_name = '{} {}'.format(customer.name, data['task_type'])
        # validate the cron data
        if not re.fullmatch(r'([1-5]?[0-9]|\*)', data['periodic_task']['minute']) or \
                not re.fullmatch(r'1?[0-9]|2[0-3]|\*', data['periodic_task']['hour']) or \
                not re.fullmatch(r'[0-6]|\*', data['periodic_task']['day_of_week']) or \
                not re.fullmatch(r'[1-9]|[1-2][0-9]|3[0-1]|\*', data['periodic_task']['day_of_month']) or \
                not re.fullmatch(r'[1-9]|1[0-2]|\*', data['periodic_task']['month_of_year']):
            raise serializers.ValidationError({'periodic_tas': 'Cron parameters are not valid'})
        # get or create the cron schedule
        cron, _ = CrontabSchedule.objects.get_or_create(**data['periodic_task'])
        # check if a periodic task with the same name already exists
        if PeriodicTask.objects.filter(name=task_name).exists():
            raise serializers.ValidationError('A periodic task with this name already exists')
        # prepare the periodic task
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
