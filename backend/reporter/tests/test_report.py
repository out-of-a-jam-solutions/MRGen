from datetime import datetime, date, timedelta
import json
import uuid

from django.contrib.auth.models import User
from rest_framework import status, test
from rest_framework.reverse import reverse

from reporter import models


class ReportListRequestTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_list_status_code(self):
        """
        Tests the response's status code for 200 OK.
        """
        # request
        response = self.client.get(reverse(self.view_name))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list(self):
        """
        Tests that reports are listed if they exist in the database.
        """
        # create reports
        report_1 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 1, 1), end_date=date(2019, 1, 31))
        report_2 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 2, 1), end_date=date(2019, 2, 28))
        # request
        response = self.client.get(reverse(self.view_name))
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(response_body), dict)
        self.assertEqual(len(response_body['results']), 2)
        self.assertIn(
            {
                'pk': report_1.id,
                'customer': self.customer.id,
                'start_date': '2019-01-01',
                'end_date': '2019-01-31',
                'date_generated': datetime.now().date().strftime('%Y-%m-%d')
            },
            response_body['results']
        )
        self.assertIn(
            {
                'pk': report_2.id,
                'customer': self.customer.id,
                'start_date': '2019-02-01',
                'end_date': '2019-02-28',
                'date_generated': datetime.now().date().strftime('%Y-%m-%d')
            },
            response_body['results']
        )

    def test_list_none(self):
        """
        Tests that no reports are listed if none exist in the database.
        """
        # request
        response = self.client.get(reverse(self.view_name))
        repsonse_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(repsonse_body), dict)
        self.assertEqual(len(repsonse_body['results']), 0)

    def test_list_pagination(self):
        """
        Tests that pagination works properly.
        """
        # create reports
        report_1 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 1, 1), end_date=date(2019, 1, 31))
        report_2 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 2, 1), end_date=date(2019, 2, 28))
        # request
        response = self.client.get(reverse(self.view_name), {'page': '1', 'page_size': '1'})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(type(response_body), dict)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn(
            {
                'pk': report_2.id,
                'customer': self.customer.id,
                'start_date': '2019-02-01',
                'end_date': '2019-02-28',
                'date_generated': datetime.now().date().strftime('%Y-%m-%d')
            },
            response_body['results']
        )

    def test_list_pagination_meta(self):
        """
        Tests that a paginated list request includes the proper metdata.
        """
        # create reports
        report_1 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 1, 1), end_date=date(2019, 1, 31))
        models.Report.objects.create(customer=self.customer, start_date=date(2019, 2, 1), end_date=date(2019, 2, 28))
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

    def test_list_filter_id(self):
        """
        Tests that reports are listed if they match the id filter parameter.
        """
        # create reports
        report_1 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 1, 1), end_date=date(2019, 1, 31))
        report_2 = models.Report.objects.create(customer=self.customer, start_date=date(2019, 2, 1), end_date=date(2019, 2, 28))
        # request
        response = self.client.get(reverse(self.view_name), {'id': report_2.id})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn(
            {
                'pk': report_2.id,
                'customer': self.customer.id,
                'start_date': '2019-02-01',
                'end_date': '2019-02-28',
                'date_generated': datetime.now().date().strftime('%Y-%m-%d')
            },
            response_body['results']
        )

    def test_list_filter_customer(self):
        """
        Tests that reports are listed if they match the customer id filter parameter.
        """
        # create a second customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create reports
        models.Report.objects.create(customer=self.customer, start_date=date(2019, 1, 1), end_date=date(2019, 1, 31))
        report_2 = models.Report.objects.create(customer=customer_2, start_date=date(2019, 2, 1), end_date=date(2019, 2, 28))
        # request
        response = self.client.get(reverse(self.view_name), {'customer': report_2.customer.id})
        response_body = json.loads(response.content.decode('utf-8'))
        # test response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_body['results']), 1)
        self.assertIn(
            {
                'pk': report_2.id,
                'customer': customer_2.id,
                'start_date': '2019-02-01',
                'end_date': '2019-02-28',
                'date_generated': datetime.now().date().strftime('%Y-%m-%d')
            },
            response_body['results']
        )


class ReportCreateRequestTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_status_code(self):
        """
        Tests the response's status code for 201 CREATED.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_customer(self):
        """
        Tests that the customer field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().customer_id, request_body['customer'])

    def test_customer_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid customer ID.
        """
        # request
        request_body = {
            'customer': -1,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_date(self):
        """
        Tests that the start date field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().start_date.strftime('%Y-%m-%d'), request_body['start_date'])

    def test_start_date_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid start date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-02-32',
            'end_date': '2019-03-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_date_future(self):
        """
        Tests the response's status code for 400 BAD REQUEST given a start date in the future.
        """
        # create the bad start date
        start_date = datetime.now() + timedelta(days=7)
        start_date = start_date.date().strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': start_date,
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_date(self):
        """
        Tests that the end date field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().end_date.strftime('%Y-%m-%d'), request_body['end_date'])

    def test_end_date_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid start date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-02-01',
            'end_date': '2019-02-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_date_future(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an end date in the future.
        """
        # create the bad start date
        end_date = datetime.now() + timedelta(days=7)
        end_date = end_date.date().strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': end_date
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_start_date_after_end_date(self):
        """
        Tests the response's status code for 400 BAD REQUEST given a start date that is after the end date.
        """
        # create the bad start and end date
        end_date = date(2019, 1, 1).strftime('%Y-%m-%d')
        start_date = date(2019, 1, 2).strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': start_date,
            'end_date': end_date
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReportCreateReportTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_create_object(self):
        """
        Tests that a Report object was created.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.exists())

    def test_customer(self):
        """
        Tests that a Report object assigns the right customer.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(customer=request_body['customer']).exists())

    def test_start_date(self):
        """
        Tests that a Report object assigns the right start date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(start_date=date(2019, 1, 1)).exists())

    def test_end_date(self):
        """
        Tests that a Report object assigns the right end date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(end_date=date(2019, 1, 31)).exists())

    def test_date_generated(self):
        """
        Tests that a Report object assigns the right generated date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(date_generated=datetime.now().date()).exists())

    def test_num_mac_os(self):
        """
        Tests that a Report object assigns the right number of mac os computers and not other os types.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_num_windows_os(self):
        """
        Tests that a Report object assigns the right number of windows os computers and not other os types.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_num_linux_os(self):
        """
        Tests that a Report object assigns the right number of linux os computers and not other os types.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)

    def test_num_mac_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of mac os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_num_mac_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of mac os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_num_windows_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_num_windows_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_num_linux_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)

    def test_num_linux_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)


class ReportCreateSubReportTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_create_object(self):
        """
        Tests that a SubReport object is created.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.exists())
        self.assertEqual(models.SubReport.objects.count(), 1)

    def test_create_object_multiple(self):
        """
        Tests that multiple SubReport objects are created.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-03-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.exists())
        self.assertEqual(models.SubReport.objects.count(), 3)

    def test_create_object_multiple_cross_year(self):
        """
        Tests that multiple SubReport objects are created across different years.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2017-11-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.exists())
        self.assertEqual(models.SubReport.objects.count(), 16)

    def test_start_end_date(self):
        """
        Tests that a SubReport object assigns the right start and end date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-02',
            'end_date': '2019-01-27'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().start_date, date(2019, 1, 2))
        self.assertEqual(models.SubReport.objects.first().end_date, date(2019, 1, 27))

    def test_start_end_date_multiple(self):
        """
        Tests that multiple SubReport objects are assigned the right start and end date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-03',
            'end_date': '2019-03-18'
        }
        self.client.post(reverse(self.view_name), request_body)

        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 3), end_date=date(2019, 1, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 3, 1), end_date=date(2019, 3, 18)).exists())

    def test_start_end_dates_multiple_cross_year(self):
        """
        Tests that multiple SubReport across multiple years are assigned the right start and end date.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2017-11-19',
            'end_date': '2019-02-20'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2017, 11, 19), end_date=date(2017, 11, 30)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2017, 12, 1), end_date=date(2017, 12, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 1, 1), end_date=date(2018, 1, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 2, 1), end_date=date(2018, 2, 28)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 3, 1), end_date=date(2018, 3, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 4, 1), end_date=date(2018, 4, 30)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 5, 1), end_date=date(2018, 5, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 6, 1), end_date=date(2018, 6, 30)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 7, 1), end_date=date(2018, 7, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 8, 1), end_date=date(2018, 8, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 9, 1), end_date=date(2018, 9, 30)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 10, 1), end_date=date(2018, 10, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 11, 1), end_date=date(2018, 11, 30)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2018, 12, 1), end_date=date(2018, 12, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31)).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 20)).exists())

    def test_report(self):
        """
        Tests that a SubReport object assigns the right report.
        """
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        report = models.Report.objects.first()
        self.assertTrue(models.SubReport.objects.filter(report=report).exists())

    def test_warnings_unresolved_start(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_start, 2)

    def test_warnings_unresolved_start_exclude_resolved(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings when past resolved warnings exist.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2018, 12, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_start, 2)

    def test_warnings_unresolved_start_include_resolved(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings when future resolved warnings exist.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_start, 3)

    def test_warnings_unresolved_start_multiple_customers(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings when there are multiple customers.
        """
        # create a new customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(customer_2, comp, date_reported=date(2018, 12, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_start, 2)

    def test_warnings_unresolved_start_cross_month(self):
        """
        Tests that multiple SubReports assign the right number of starting unresolved warnings to each.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_start=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_start=5).exists())

    def test_warnings_unresolved_start_cross_month_exclude_resolved(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings when past resolved warnings exist across multiple SubReports.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2018, 12, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3), date_resolved=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_start=1).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_start=3).exists())

    def test_warnings_unresolved_start_cross_month_include_resolved(self):
        """
        Tests that a SubReport assigns the right number of starting unresolved warnings when future resolved warnings exist across multiple SubReports.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2019, 1, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3), date_resolved=date(2019, 2, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_start=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_start=4).exists())

    def test_warnings_unresolved_end(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_end, 2)

    def test_warnings_unresolved_end_exclude_resolved(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings when past resolved warnings exist.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_end, 2)

    def test_warnings_unresolved_end_include_resolved(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings when future resolved warnings exist.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2019, 2, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_end, 3)

    def test_warnings_unresolved_end_multiple_customers(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings when there are multiple customers.
        """
        # create a new customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4))
        create_watchman_warning(customer_2, comp, date_reported=date(2018, 12, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_unresolved_end, 2)

    def test_warnings_unresolved_end_cross_month(self):
        """
        Tests that multiple SubReports assign the right number of ending unresolved warnings to each.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 5))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_end=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_end=5).exists())

    def test_warnings_unresolved_end_cross_month_exclude_resolved(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings when past resolved warnings exist across multiple SubReports.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 5), date_resolved=date(2019, 1, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3), date_resolved=date(2019, 2, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_end=1).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_end=3).exists())

    def test_warnings_unresolved_end_cross_month_include_resolved(self):
        """
        Tests that a SubReport assigns the right number of ending unresolved warnings when future resolved warnings exist across multiple SubReports.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 5), date_resolved=date(2019, 2, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3), date_resolved=date(2019, 3, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_unresolved_end=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_unresolved_end=4).exists())

    def test_warnings_created(self):
        """
        Tests that a SubReport assigns the right number of created warnings.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # create the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_created, 2)

    def test_warnings_created_multiple_customers(self):
        """
        tests that a SubReport assigns the right number of created warnings when there are multiple customers.
        """
        # create a new customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(customer_2, comp, date_reported=date(2019, 1, 4))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_created, 2)

    def test_warnings_created_cross_month(self):
        """
        Tests that multiple SubReports assign the right number of created warnings to each.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 4))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 2, 5))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_created=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_created=3).exists())

    def test_warnings_resolved(self):
        """
        Tests that a SubReport assigns the right number of resolved warnings.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4), date_resolved=date(2019, 1, 9))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 5), date_resolved=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_resolved, 2)

    def test_warnings_resolved_multiple_customers(self):
        """
        Tests that a SubReport assigns the right number of resolved warnings when there are mutliple customers.
        """
        # create a new customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 3), date_resolved=date(2019, 1, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2019, 1, 4), date_resolved=date(2019, 1, 10))
        create_watchman_warning(customer_2, comp, date_reported=date(2019, 1, 4), date_resolved=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.first().num_warnings_resolved, 2)

    def test_warnings_resolved_cross_month(self):
        """
        Tests that multiple SubReports assign the right number of resolved warnings to each.
        """
        # create the computers
        comp = create_watchman_computer(self.customer)
        # cerate the warnings
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3), date_resolved=date(2019, 1, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4), date_resolved=date(2019, 1, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 3), date_resolved=date(2019, 2, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 4), date_resolved=date(2019, 2, 10))
        create_watchman_warning(self.customer, comp, date_reported=date(2018, 12, 5), date_resolved=date(2019, 2, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 1, 1), end_date=date(2019, 1, 31), num_warnings_resolved=2).exists())
        self.assertTrue(models.SubReport.objects.filter(start_date=date(2019, 2, 1), end_date=date(2019, 2, 28), num_warnings_resolved=3).exists())


class ReportCreateComputerReportTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-lc'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_create_object(self):
        """
        Tests that ComputerReport objects are created.
        """
        # create the computers
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.count(), 2)

    def test_create_object_multiple_customers(self):
        """
        Tests that the right number of computer report objects are created when there are multiple customers.
        """
        # create the customer
        customer_2 = models.Customer.objects.create(name='customer 2', watchman_group_id='g_2222222', repairshopr_id='2222222')
        # create the computers
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        create_watchman_computer(customer_2, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.count(), 2)

    def test_create_object_exclude_reported_in_past(self):
        """
        Tests that computers that were not reported anytime after the start date are not included.
        """
        # create the computers
        comp_1 = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        comp_2 = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 11))
        comp_bad = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 31))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.ComputerReport.objects.filter(id=comp_1.id).exists())
        self.assertTrue(models.ComputerReport.objects.filter(id=comp_2.id).exists())
        self.assertFalse(models.ComputerReport.objects.filter(id=comp_bad.id).exists())

    def test_name(self):
        """
        Tests that the name is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().name, comp.name)

    def test_os_type(self):
        """
        Tests that the OS type is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().os_type, comp.os_type)

    def test_os_version(self):
        """
        Tests that the OS version is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().os_version, comp.os_version)

    def test_ram_gb(self):
        """
        Tests that the amount of RAM is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().ram_gb, comp.ram_gb)

    def test_hdd_capacity_gb(self):
        """
        Tests that the HDD capacity is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().hdd_capacity_gb, comp.hdd_capacity_gb)

    def test_hdd_usage_gb(self):
        """
        Tests that the HDD usage is set properly in a ComputerReport.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().hdd_usage_gb, comp.hdd_usage_gb)

    def test_report(self):
        """
        Tests that the report is WatchmanComputer's report is assigned the right foreign key.
        """
        # create the computers
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        report = models.Report.objects.first()
        self.assertEqual(models.ComputerReport.objects.filter(report=report).count(), 2)

    def test_computer(self):
        """
        Tests that the WatchmanComputer's computer is assigned the right forign key.
        """
        # create the computers
        comp = create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # request
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.first().computer, comp)


class ReportDeleteTest(test.APITestCase):
    def setUp(self):
        # create test user
        self.username = 'test'
        self.password = 'test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
        # retrieve the view
        self.view_name = 'reporter:report-d'
        # add customer to database
        models.Customer(name='customer 1', watchman_group_id='g_1111111', repairshopr_id='1111111').save()
        self.customer = models.Customer.objects.first()

    def test_status_code(self):
        """
        Tests that the request returns status code 204 NO CONTENT.
        """
        # create the report
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse('reporter:report-lc'), request_body)
        # request
        report = models.Report.objects.first()
        response = self.client.delete(reverse(self.view_name, args=[report.id]))
        # test response
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_report_object(self):
        """
        Tests that the Report objects are deleted.
        """
        # create the report
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse('reporter:report-lc'), request_body)
        # request
        report = models.Report.objects.first()
        self.client.delete(reverse(self.view_name, args=[report.id]), request_body)
        # test database
        self.assertEqual(models.Report.objects.count(), 0)

    def test_sub_report_object(self):
        """
        Tests that the SubReport objects are deleted.
        """
        # create the report
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse('reporter:report-lc'), request_body)
        # request
        report = models.Report.objects.first()
        self.client.delete(reverse(self.view_name, args=[report.id]), request_body)
        # test database
        self.assertEqual(models.SubReport.objects.count(), 0)

    def test_computer_report_object(self):
        """
        Tests that the ComputerReport objects are deleted.
        """
        # create the computers
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        create_watchman_computer(self.customer, date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 10))
        # create the report
        request_body = {
            'customer': self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-02-28'
        }
        self.client.post(reverse('reporter:report-lc'), request_body)
        # request
        report = models.Report.objects.first()
        self.client.delete(reverse(self.view_name, args=[report.id]), request_body)
        # test database
        self.assertEqual(models.ComputerReport.objects.count(), 0)

def create_watchman_computer(customer, computer_id=None, name=None, date_reported=None, date_last_reported=None, os_type='mac', os_version='OS X 10.13.6', ram_gb=2, hdd_capacity_gb=100, hdd_usage_gb=50):
    """
    Helper function to create watchman computers in a similar fassion to the Celery tasks.
    """
    # generate unique names and IDs if necessary
    identifier = str(uuid.uuid1())
    if not computer_id:
        computer_id = identifier
    if not name:
        name = identifier
    # setup the new computer
    comp = models.WatchmanComputer(watchman_group_id=customer,
                                   computer_id=computer_id,
                                   name=name,
                                   os_type=os_type,
                                   os_version=os_version,
                                   ram_gb=ram_gb,
                                   hdd_capacity_gb=hdd_capacity_gb,
                                   hdd_usage_gb=hdd_usage_gb
                                  )
    comp.save()
    # adjust dates after creation
    if date_reported:
        comp.date_reported = date_reported
    if date_last_reported:
        comp.date_last_reported = date_last_reported
    comp.save()
    # return the created date
    return comp

def create_watchman_warning(customer, computer, date_reported=None, date_last_checked=None, date_resolved=None, warning_id=None, name='warning', details='details'):
    """
    Helper function to create watchman warnings in a similar fassion to the Celery tasks.
    """
    # generate unique names and IDs if necessary
    identifier = str(uuid.uuid1())
    if not warning_id:
        warning_id = identifier
    # setup the new computer
    warn = models.WatchmanWarning(watchman_group_id=customer,
                                  computer_id=computer,
                                  warning_id = identifier,
                                  date_resolved=date_resolved,
                                  name=name,
                                  details=details
                                 )
    warn.save()
    # adjust dates after creation
    if date_reported:
        warn.date_reported = date_reported
    if date_last_checked:
        warn.date_last_checked = date_last_checked
    warn.save()
    # return the created date
    return warn
