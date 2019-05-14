from datetime import date
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

    def test_report_create_status_code(self):
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
