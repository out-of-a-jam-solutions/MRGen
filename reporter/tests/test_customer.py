import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from reporter import models


class CustomerLCTest(APITestCase):
    def setUp(self):
        # create test user with permissions
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
        self.assertEqual(len(response_body['data']), len(customers))
        for customer in customers:
            self.assertIn({
                'pk': customer.id,
                'name': customer.name,
                'watchman_group_id': customer.watchman_group_id,
                'repairshopr_id': customer.repairshopr_id
            }, response_body['data'])

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
