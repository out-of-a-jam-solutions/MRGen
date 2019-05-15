from datetime import datetime

from rest_framework import response, status, views

from reporter import models


class ReportLCView(views.APIView):
    def post(self, request, format=None):
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
        # create the report
        models.Report.objects.create(customer=customer, start_date=start_date, end_date=end_date)
        # return the success response
        return response.Response(status=status.HTTP_201_CREATED)
