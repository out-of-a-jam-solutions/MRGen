from celery.result import result_from_tuple
from rest_framework import views
from rest_framework import generics
from rest_framework import response

from backend.reporter import models, serializers, tasks_watchman


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
    queryset = models.Customer.objects.all()
    filterset_fields = ('id', 'name', 'watchman_group_id', 'repairshopr_id')


class CustomerRDView(generics.RetrieveDestroyAPIView):  # pylint: disable=too-many-ancestors
    lookup_field = 'pk'
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
