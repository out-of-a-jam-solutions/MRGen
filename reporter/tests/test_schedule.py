import json

from django.contrib.auth.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import test

from reporter import models


class ScheduleCreateTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:schedule-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_schedule_create_schedule(self):
        """
        Tests that the schedule endpoint successfully creates a schedule object.
        """
        # request
        request_body = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'watchman'
        }
        self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        self.assertTrue(models.Schedule.objects.exists())
        schedule = models.Schedule.objects.first()
        self.assertEqual(schedule.customer_id, request_body['customer'])

    def test_schedule_create_crontab(self):
        """
        Tests that a crontab is created for the schedule.
        """
        # request
        request_body = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'watchman'
        }
        self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        cron = CrontabSchedule.objects.first()
        cron_vals = {
                'minute': cron.minute,
                'hour': cron.hour,
                'day_of_week': cron.day_of_week,
                'day_of_month': cron.day_of_month,
                'month_of_year': cron.month_of_year,
        }
        self.assertEqual(cron_vals, request_body['periodic_task'])
