import math

from rest_framework import pagination
from rest_framework import response


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        # calculate the total number of pages given the query parameters
        page_count = math.ceil(self.page.paginator.count / self.page.paginator.per_page)
        # build the request response
        return response.Response({
            'results': data,
            'results_count': self.page.paginator.count,
            'page': self.page.number,
            'page_count': page_count,
            'page_size': self.page.paginator.per_page,
            'page_next': self.get_next_link(),
            'page_previous': self.get_previous_link()
        })
