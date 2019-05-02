import json

from django.contrib.auth.models import User
from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import test

from backend.reporter import models


class CustomerLCTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:customer-lc'

    def test_customer_list(self):
        # add customers to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222').save()
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        customers = models.Customer.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), len(customers))
        for customer in customers:
            self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
            }, response_body['results'])

    def test_customer_list_filter_id(self):
        # add customers to database
        customer = models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111')
        customer.save()
        models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222').save()
        # request
        response = self.client.get(reverse(self.view_name), {'id': customer.id})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
        }, response_body['results'])

    def test_customer_list_filter_name(self):
        # add customers to database
        customer = models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111')
        customer.save()
        models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222').save()
        # request
        response = self.client.get(reverse(self.view_name), {'name': customer.name})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
        }, response_body['results'])

    def test_customer_list_filter_watchman_group_id(self):
        # add customers to database
        customer = models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111')
        customer.save()
        models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222').save()
        # request
        response = self.client.get(reverse(self.view_name), {'watchman_group_id': customer.watchman_group_id})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
        }, response_body['results'])

    def test_customer_list_filter_repairshopr_id(self):
        # add customers to database
        customer = models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111')
        customer.save()
        models.Customer(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222').save()
        # request
        response = self.client.get(reverse(self.view_name), {'repairshopr_id': customer.repairshopr_id})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
        }, response_body['results'])

    def test_customer_create(self):
        # request
        request_body = {
            'name': 'customer 1',
            'watchman_group_id': 'g_1111111',
            'repairshopr_id': '1111111'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        # test database
        customer = models.Customer.objects.first()
        self.assertDictEqual({
            'name': customer.name,
            'watchman_group_id': customer.watchman_group_id,
            'repairshopr_id': customer.repairshopr_id
        }, request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(request_body, response_body)


class CustomerRDTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:customer-rd'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_customer_read(self):
        # request
        response = self.client.get(reverse(self.view_name, args=[self.customer.id]))
        response_body = json.loads(response.content.decode('utf-8'))
        # test repsonse
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response_body, {
            'pk': self.customer.id,
            'name': self.customer.name,
            'watchman_group_id': self.customer.watchman_group_id,
            'repairshopr_id': self.customer.repairshopr_id
        })

    def test_customer_delete(self):
        # request
        response = self.client.delete(reverse(self.view_name, args=[self.customer.id]))
        # test database
        customers = models.Customer.objects.all()
        self.assertNotIn(self.customer, customers)
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_customer_delete_associated_schedules(self):
        """
        Tests that deleting a customer also deletes any associated schedules.
        """
        # create schedule
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
        self.client.post(reverse('reporter:schedule-lc'), request_body, format='json')
        # request
        self.client.delete(reverse(self.view_name, args=[self.customer.id]))
        # test database
        self.assertFalse(models.Schedule.objects.exists())

    def test_customer_delete_associated_periodic_tasks(self):
        """
        Tests that deleting a customer also deletes any associated periodic tasks.
        """
        # create schedule
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
        self.client.post(reverse('reporter:schedule-lc'), request_body, format='json')
        # request
        self.client.delete(reverse(self.view_name, args=[self.customer.id]))
        # test database
        self.assertFalse(PeriodicTask.objects.exists())
