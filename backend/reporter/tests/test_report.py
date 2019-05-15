from datetime import datetime, date, timedelta
import uuid

from django.contrib.auth.models import User
from rest_framework import status, test
from rest_framework.reverse import reverse

from reporter import models


class ReportCreateTest(test.APITestCase):
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
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_report_object(self):
        """
        Tests that a Report object was created.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.exists())

    def test_report_object_customer(self):
        """
        Tests that a Report object assigns the right customer.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(customer=request_body['customer']).exists())

    def test_report_object_start_date(self):
        """
        Tests that a Report object assigns the right start date.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(start_date=date(2019, 1, 1)).exists())

    def test_report_object_end_date(self):
        """
        Tests that a Report object assigns the right end date.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(end_date=date(2019, 1, 31)).exists())

    def test_report_object_date_generated(self):
        """
        Tests that a Report object assigns the right generated date.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertTrue(models.Report.objects.filter(date_generated=datetime.now().date()).exists())

    def test_report_object_num_mac_os(self):
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
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_report_object_num_windows_os(self):
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
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_report_object_num_linux_os(self):
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
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)

    def test_report_object_num_mac_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of mac os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_report_object_num_mac_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of mac os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='mac', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_mac_os, 2)

    def test_report_object_num_windows_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_report_object_num_windows_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='windows', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_windows_os, 2)

    def test_report_object_num_linux_os_last_reported_before_start_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were last reported before the start date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2018, 12, 30))  # before start date
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 1, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)

    def test_report_object_num_linux_os_first_reported_after_end_date(self):
        """
        Tests that a Report object assigns the right number of windows os computers when some were first reported after the end date.
        """
        # create computers
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2019, 2, 15), date_last_reported=date(2019, 2, 15))  # first reported after end date
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        create_watchman_computer(self.customer, os_type='linux', date_reported=date(2018, 12, 1), date_last_reported=date(2019, 2, 15))
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().num_linux_os, 2)

    def test_report_customer(self):
        """
        Tests that the customer field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().customer_id, request_body['customer'])

    def test_report_customer_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid customer ID.
        """
        # request
        request_body = {
            'customer':  -1,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_start_date(self):
        """
        Tests that the start date field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().start_date.strftime('%Y-%m-%d'), request_body['start_date'])

    def test_report_start_date_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid start date.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': 'bad',
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_start_date_future(self):
        """
        Tests the response's status code for 400 BAD REQUEST given a start date in the future.
        """
        # create the bad start date
        start_date = datetime.now() + timedelta(days=7)
        start_date = start_date.date().strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': start_date,
            'end_date': '2019-01-31'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_end_date(self):
        """
        Tests that the end date field was set properly in the Report object.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': '2019-01-31'
        }
        self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertEqual(models.Report.objects.first().end_date.strftime('%Y-%m-%d'), request_body['end_date'])

    def test_report_end_date_bad(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an invalid start date.
        """
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': 'bad'
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_end_date_future(self):
        """
        Tests the response's status code for 400 BAD REQUEST given an end date in the future.
        """
        # create the bad start date
        end_date = datetime.now() + timedelta(days=7)
        end_date = end_date.date().strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': '2019-01-01',
            'end_date': end_date
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_report_start_date_after_end_date(self):
        """
        Tests the response's status code for 400 BAD REQUEST given a start date that is after the end date.
        """
        # create the bad start and end date
        end_date = date(2019, 1, 1).strftime('%Y-%m-%d')
        start_date = date(2019, 1, 2).strftime('%Y-%m-%d')
        # request
        request_body = {
            'customer':  self.customer.id,
            'start_date': start_date,
            'end_date': end_date
        }
        response = self.client.post(reverse(self.view_name), request_body)
        # test database
        self.assertFalse(models.Report.objects.exists())
        self.assertFalse(models.SubTimeReport.objects.exists())
        self.assertFalse(models.ComputerReport.objects.exists())
        # test response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


def create_watchman_computer(customer, computer_id=None, name=None, date_reported=None, date_last_reported=None, os_type='mac', os_version='OS X 10.13.6', ram_gb=2, hdd_capacity_gb=100, hdd_usage_gb=50):
    """
    Helper function to create watchman computers in a similar fassion to the Celery tasks.
    """
    # generate unique names and IDs if necessary
    identifier = uuid.uuid1()
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
    identifier = uuid.uuid1()
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
