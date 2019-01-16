from rest_framework import views
from rest_framework import response

from reporter import tasks


class Forward(views.APIView):
    def get(self, request):
        request = tasks.get_watchman_computers.delay(group_id=request.query_params['group_id'])
        while not request.ready():
            pass
        return response.Response(request.result[1])


