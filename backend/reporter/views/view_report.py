import calendar
from datetime import datetime, date
import tempfile

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django_weasyprint import WeasyTemplateResponseMixin
from knox.auth import TokenAuthentication
from rest_framework import generics, response, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from weasyprint import HTML

from reporter import models, serializers


class ReportLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ReportSerializer
    queryset = models.Report.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('id', 'customer')

    def post(self, request):
        """
        Create a new report for given customer and time period.
        """
        # parse the request data and build the bad request response
        bad_response = {}
        # parse the customer ID
        try:
            customer = models.Customer.objects.get(id=request.data['customer'])
        except models.Customer.DoesNotExist as e:
            bad_response['customer'] = [str(e)]
        # parse the start date
        try:
            start_date = datetime.strptime(request.data['start_date'], '%Y-%m-%d').date()
            # check that the start date is in the past
            if start_date > datetime.now().date():
                raise ValueError('Start date is after current date.')
        except ValueError as e:
            bad_response['start_date'] = [str(e)]
        # parse the end date
        try:
            end_date = datetime.strptime(request.data['end_date'], '%Y-%m-%d').date()
            # check that the end date is in the past
            if end_date > datetime.now().date():
                raise ValueError('End date is after current date.')
            # check that the end date is after the start date
            if 'start_date' not in bad_response and end_date < start_date:
                raise ValueError('End date is before the starting date.')
        except ValueError as e:
            bad_response['end_date'] = [str(e)]
        # return the error response if necessary
        if bad_response:
            return response.Response(bad_response, status=status.HTTP_400_BAD_REQUEST)

        # generate report statistics
        num_mac_os = models.WatchmanComputer.objects.filter(
            os_type='mac',
            watchman_group_id=customer,
            date_reported__lt=end_date,
            date_last_reported__gt=start_date
        ).count()
        num_windows_os = models.WatchmanComputer.objects.filter(
            os_type='windows',
            watchman_group_id=customer,
            date_reported__lt=end_date,
            date_last_reported__gt=start_date
        ).count()
        num_linux_os = models.WatchmanComputer.objects.filter(
            os_type='linux',
            watchman_group_id=customer,
            date_reported__lt=end_date,
            date_last_reported__gt=start_date
        ).count()
        # create the report
        report = models.Report.objects.create(
            customer=customer,
            start_date=start_date,
            end_date=end_date,
            num_mac_os=num_mac_os,
            num_windows_os=num_windows_os,
            num_linux_os=num_linux_os
        )

        # create all sub reports
        for start, end in report_dates(start_date, end_date):
            # count the number of warnings unresolved at the beginning of the sub report period
            num_warnings_unresolved_start = models.WatchmanWarning.objects.exclude(
                date_resolved__lt=start
            ).filter(
                watchman_group_id=customer,
                date_reported__lt=start
            ).count()
            # count the number of warnings unresolved at the end of the sub report period
            num_warnings_unresolved_end = models.WatchmanWarning.objects.exclude(
                date_resolved__lte=end
            ).filter(
                watchman_group_id=customer,
                date_reported__lte=end
            ).count()
            # count the number of warnings created during the sub report period
            num_warnings_created = models.WatchmanWarning.objects.filter(
                watchman_group_id=customer,
                date_reported__gte=start,
                date_reported__lte=end
            ).count()
            # cound the number of warnings resolved during the sub report period
            num_warnings_resolved = models.WatchmanWarning.objects.filter(
                watchman_group_id=customer,
                date_resolved__gte=start,
                date_resolved__lte=end
            ).count()
            # create the subreport
            models.SubReport.objects.create(
                report=report,
                start_date=start,
                end_date=end,
                num_warnings_unresolved_start=num_warnings_unresolved_start,
                num_warnings_unresolved_end=num_warnings_unresolved_end,
                num_warnings_created=num_warnings_created,
                num_warnings_resolved=num_warnings_resolved
            )

        # created the computer reports
        for computer in models.WatchmanComputer.objects.filter(
            watchman_group_id=customer,
            date_last_reported__gte=start_date
        ).all():
            models.ComputerReport.objects.create(
                name=computer.name,
                os_type=computer.os_type,
                os_version=computer.os_version,
                ram_gb=computer.ram_gb,
                hdd_capacity_gb=computer.hdd_capacity_gb,
                hdd_usage_gb=computer.hdd_usage_gb,
                report=report,
                computer=computer
            )

        # return the success response
        return response.Response(status=status.HTTP_201_CREATED)


class ReportDeleteView(generics.DestroyAPIView):
    lookup_field = 'pk'
    queryset = models.Report.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class ReportDetailView(DetailView):
    model = models.Report
    template_name = 'report.html'


class ReportPDFView(WeasyTemplateResponseMixin, ReportDetailView):
    pdf_attachment = False
    pdf_filename = 'report.pdf'


def days_in_month(year, month):
    """
    A helper function that takes in month and year numbers and returns the number of day in the month.
    """
    return calendar.monthrange(year, month)[1]

def report_dates(start_date, end_date):
    """
    Generator function to create a range of report dates given a start and end date.
    """
    # iterate over every year within date range
    for year in range(start_date.year, end_date.year + 1):
        # find the month range for the year
        month_range = range(1, 13)
        # start and end year cases
        if year == start_date.year:
            month_range = range(start_date.month, 13)
        elif year == end_date.year:
            month_range = range(1, end_date.month + 1)
        # single year case
        if start_date.year == end_date.year:
            month_range = range(start_date.month, end_date.month + 1)
        # iterate over every month in the year
        for month in month_range:
            # find the day range for the year
            day_range = (1, days_in_month(year, month))
            # start and end month cases
            if year == start_date.year and month == start_date.month:
                day_range = (start_date.day, days_in_month(year, month))
            elif year == end_date.year and month == end_date.month:
                day_range = (1, end_date.day)
            # single month case
            if start_date.year == end_date.year and start_date.month == end_date.month:
                day_range = (start_date.day, end_date.day)
            # create the sub reports
            yield (date(year, month, day_range[0]), date(year, month, day_range[1]))
