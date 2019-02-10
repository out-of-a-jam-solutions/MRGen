from celery.result import result_from_tuple
from rest_framework import views
from rest_framework import response

from reporter import tasks_watchman


class Forward(views.APIView):
    def get(self, request):
        # get watchman concatenated results
        results = tasks_watchman.update_client(request.query_params['watchman_group_id'])
        results = result_from_tuple(results.get())
        results = results.get()

        return response.Response(results)
