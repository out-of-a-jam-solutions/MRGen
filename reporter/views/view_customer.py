from celery.result import result_from_tuple
from rest_framework import views
from rest_framework import generics
from rest_framework import response

from reporter import models, serializers, tasks_watchman


class Forward(views.APIView):
    def get(self, request):
        # get watchman concatenated results
        results = tasks_watchman.update_client(request.query_params['watchman_group_id'])
        results = result_from_tuple(results.get())
        results = results.get()

        return response.Response(results)


class CustomerLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.CustomerSerializer

    def get_queryset(self):
        return models.Customer.objects.all()

    def list(self, request, *args, **kwargs):
        new_response = super(CustomerLCView, self).list(request, *args, **kwargs)
        # wrap array of results in JSON object
        new_response.data = {
            'data': new_response.data
        }
        return new_response
