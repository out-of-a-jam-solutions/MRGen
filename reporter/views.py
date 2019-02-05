from celery.result import result_from_tuple
from rest_framework import views
from rest_framework import response

from reporter import tasks_watchman


class Forward(views.APIView):
    def get(self, request):
        # get watchman concatenated results
        results = tasks_watchman.watchman_update_client(request.query_params['watchman_group_id'])
        res = result_from_tuple(results.get())
        results = res.get()
        # save warnings to database
        tasks_watchman.parse_warnings(results)

        return response.Response(results)
