import json

from django.contrib.auth.models import User
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from rest_framework import status, test
from rest_framework.reverse import reverse

from reporter import models


class ScheduleListTest(test.APITestCase):
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

    def test_schedule_list(self):
        """
        Tests that schedules are listed if they exist in the database.
        """
        # create schedules
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
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(response_body), dict)
        self.assertEqual(len(response_body['results']), 1)
        self.assertDictContainsSubset(request_body, response_body['results'][0])

    def test_schedule_list_status_code(self):
        """
        Tests the responses status code for 200 OK.
        """
        # create schedules
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
        # request
        response = self.client.get(reverse(self.view_name))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_schedule_list_none(self):
        """
        Tests that no schedules are listed if none exist in the database.
        """
        # request
        response = self.client.get(reverse(self.view_name))
        repsonse_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(repsonse_body), dict)
        self.assertEqual(len(repsonse_body['results']), 0)

    def test_schedule_list_pagination(self):
        """
        Tests that schedules are listed if they exist in the database.
        """
        # create schedules
        request_body_1 = {
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
        request_body_2 = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'repairshopr'
        }
        self.client.post(reverse(self.view_name), request_body_1, format='json')
        self.client.post(reverse(self.view_name), request_body_2, format='json')
        # request
        response = self.client.get(reverse(self.view_name), {'page': '2', 'page_size': '1'})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(response_body), dict)
        self.assertEqual(len(response_body['results']), 1)
        self.assertDictContainsSubset(request_body_2, response_body['results'][0])

    def test_schedule_list_pagination_meta(self):
        """
        Tests that a paginated list request includes the proper metdata.
        """
        # create schedules
        request_body_1 = {
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
        request_body_2 = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'repairshopr'
        }
        self.client.post(reverse(self.view_name), request_body_1, format='json')
        self.client.post(reverse(self.view_name), request_body_2, format='json')
        # request
        response = self.client.get(reverse(self.view_name), {'page_size': '1'})
        repsonse_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertIn('page', repsonse_body)
        self.assertEqual(repsonse_body['page'], 1)
        self.assertIn('page_count', repsonse_body)
        self.assertEqual(repsonse_body['page_count'], 2)
        self.assertIn('page_size', repsonse_body)
        self.assertEqual(repsonse_body['page_size'], 1)
        self.assertIn('page_next', repsonse_body)
        self.assertIn('page_previous', repsonse_body)
        self.assertIn('results_count', repsonse_body)
        self.assertEqual(repsonse_body['results_count'], 2)

    def test_schedule_list_filter_id(self):
        """
        Tests that schedules are listed if they match the id filter parameter.
        """
        # create schedules
        request_body_1 = {
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
        request_body_2 = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'repairshopr'
        }
        response = self.client.post(reverse(self.view_name), request_body_1, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        self.client.post(reverse(self.view_name), request_body_2, format='json')
        # request
        response = self.client.get(reverse(self.view_name), {'id': response_body['pk']})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertDictContainsSubset(request_body_1, response_body['results'][0])

    def test_schedule_list_filter_customer(self):
        """
        Tests that schedules are listed if they match the id filter parameter.
        """
        customer = models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        customer.save()
        # create schedules
        request_body_1 = {
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
        request_body_2 = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': customer.id,
            'task_type': 'repairshopr'
        }
        response = self.client.post(reverse(self.view_name), request_body_1, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        self.client.post(reverse(self.view_name), request_body_2, format='json')
        # request
        response = self.client.get(reverse(self.view_name), {'customer': response_body['customer']})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertDictContainsSubset(request_body_1, response_body['results'][0])

    def test_schedule_list_filter_task_type(self):
        """
        Tests that schedules are listed if they match the id filter parameter.
        """
        # create schedules
        request_body_1 = {
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
        request_body_2 = {
            'periodic_task': {
                'minute': '0',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'repairshopr'
        }
        response = self.client.post(reverse(self.view_name), request_body_1, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        self.client.post(reverse(self.view_name), request_body_2, format='json')
        # request
        response = self.client.get(reverse(self.view_name), {'task_type': response_body['task_type']})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertDictContainsSubset(request_body_1, response_body['results'][0])

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

    def test_schedule_create_status_code(self):
        """
        Tests the responses status code for 201 CREATED.
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
        response = self.client.post(reverse(self.view_name), request_body, format='json')
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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
        self.assertTrue(models.ServiceSchedule.objects.exists())
        schedule = models.ServiceSchedule.objects.first()
        self.assertEqual(schedule.customer_id, request_body['customer'])

    def test_schedule_create_periodic_task_watchman(self):
        """
        Tests that a Watchman periodic task is created for the schedule.
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
        task = PeriodicTask.objects.first()
        cron = CrontabSchedule.objects.first()
        self.assertEqual(task.crontab, cron)
        self.assertEqual(task.task, 'reporter.tasks_watchman.update_client')
        self.assertEqual(task.args, f'["{self.customer.watchman_group_id}"]')

    def test_schedule_create_periodic_task_repairshopr(self):
        """
        Tests that a RepairShopr periodic task is created for the schedule.
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
            'task_type': 'repairshopr'
        }
        self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        task = PeriodicTask.objects.first()
        cron = CrontabSchedule.objects.first()
        self.assertEqual(task.crontab, cron)
        self.assertEqual(task.task, 'reporter.tasks_repairshopr.update_client')
        self.assertEqual(task.args, f'["{self.customer.repairshopr_id}"]')

    def test_schedule_create_periodic_task_invalid_type(self):
        """
        Tests that nothing is not created when an invalid type is given.
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
            'task_type': 'invalid'
        }
        response = self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        schedule = models.ServiceSchedule.objects.first()
        task = PeriodicTask.objects.first()
        self.assertEqual(schedule, None)
        self.assertEqual(task, None)
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_schedule_create_periodic_task_no_customer_watchman(self):
        """
        Tests that a Watchman periodic task is not created if the customer has no Watchman ID.
        """
        # set customer's watchman ID to None
        self.customer.watchman_group_id = None
        self.customer.save()
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
        response = self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        self.assertFalse(PeriodicTask.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_schedule_create_periodic_task_no_customer_repairshopr(self):
        """
        Tests that a RepairShopr periodic task is not created if the customer has no RepairShopr ID.
        """
        # set customer's watchman ID to None
        self.customer.repairshopr_id = None
        self.customer.save()
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
            'task_type': 'repairshopr'
        }
        response = self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        self.assertFalse(PeriodicTask.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_schedule_create_crontab_invalid(self):
        """
        Tests nothing is created if the crontab entry is invalid.
        """
        # request
        request_body = {
            'periodic_task': {
                'minute': '61',
                'hour': '2',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
            },
            'customer': self.customer.id,
            'task_type': 'watchman'
        }
        response = self.client.post(reverse(self.view_name), request_body, format='json')
        # test database
        schedule = models.ServiceSchedule.objects.first()
        task = PeriodicTask.objects.first()
        cron = CrontabSchedule.objects.first()
        self.assertEqual(schedule, None)
        self.assertEqual(task, None)
        self.assertEqual(cron, None)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ScheduleRetrieveTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.lc_view_name = 'reporter:schedule-lc'
        self.view_name = 'reporter:schedule-rd'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_schedule_retrieve_schedule(self):
        """
        Tests that schedules can be retrieved individually.
        """
        # create schedules
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
        response = self.client.post(reverse(self.lc_view_name), request_body, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        # request
        response = self.client.get(reverse(self.view_name, args=[response_body['pk']]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(response_body), dict)
        self.assertDictContainsSubset(request_body, response_body)

    def test_schedule_retrieve_schedule_status_code(self):
        """
        Tests that status code is correct for retrieving a single schedule.
        """
        # create schedules
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
        response = self.client.post(reverse(self.lc_view_name), request_body, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        # request
        response = self.client.get(reverse(self.view_name, args=[response_body['pk']]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_schedule_retrieve_schedule_none(self):
        """
        Tests that a 404 error is thrown when no schedule exists.
        """
        # request
        response = self.client.get(reverse(self.view_name, args=[1]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ScheduleDestroyTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.lc_view_name = 'reporter:schedule-lc'
        self.view_name = 'reporter:schedule-rd'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_schedule_destroy_status_code(self):
        """
        Tests that deleting a schedule returns a 204 NO CONTENT.
        """
        # create schedules
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
        response = self.client.post(reverse(self.lc_view_name), request_body, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        # request
        response = self.client.delete(reverse(self.view_name, args=[response_body['pk']]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_schedule_destroy_schedule(self):
        """
        Tests that a schedule is destroyed.
        """
        # create schedules
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
        response = self.client.post(reverse(self.lc_view_name), request_body, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        # request
        self.client.delete(reverse(self.view_name, args=[response_body['pk']]))
        # test database
        self.assertFalse(models.ServiceSchedule.objects.exists())

    def test_schedule_destroy_periodic_task(self):
        """
        Tests that a periodic task associated with a schedule is destroyed.
        """
        # create schedules
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
        response = self.client.post(reverse(self.lc_view_name), request_body, format='json')
        response_body = json.loads(response.content.decode('utf-8'))
        # request
        self.client.delete(reverse(self.view_name, args=[response_body['pk']]))
        # test database
        self.assertFalse(PeriodicTask.objects.exists())
