import math

from celery import group
from rest_framework import views
from rest_framework import response

from reporter import tasks


class Forward(views.APIView):
    def get(self, request):
        # get watchman group information about number of computers
        watchman_group = tasks.get_watchman_group(request.query_params['group_id'])

        # put the the multiple computer requests in a group
        results_per_page = 10
        request_num = math.ceil(watchman_group['visible_computer_count'] / results_per_page) + 1
        computers_group = group(tasks.get_watchman_computers.s(page=page,
                                                               per_page=results_per_page,
                                                               group_id=request.query_params['group_id'])
                                for page in range(1, request_num))
        results = computers_group()
        new_results = list()
        while not results.ready():
            pass
        for r in results.results:
            new_results += r.result
        return response.Response(new_results)
