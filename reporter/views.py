from celery.result import result_from_tuple
from rest_framework import views
from rest_framework import response

from reporter import tasks


class Forward(views.APIView):
    def get(self, request):
        results = tasks.watchman_update_client(request.query_params['group_id'])
        res = result_from_tuple(results.get())
        return response.Response(res.get())
