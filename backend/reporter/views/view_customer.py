from celery.result import result_from_tuple
from knox.auth import TokenAuthentication
from rest_framework import generics, response, views
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from reporter import models, serializers, tasks_watchman


class CustomerLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('id', 'name', 'watchman_group_id', 'repairshopr_id')


class CustomerRDView(generics.RetrieveDestroyAPIView):  # pylint: disable=too-many-ancestors
    lookup_field = 'pk'
    serializer_class = serializers.CustomerSerializer
    queryset = models.Customer.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        # get all schedules associated with the customer and delete them
        # this would be better done by django's post_delete signal
        schedules = models.ServiceSchedule.objects.filter(customer=instance).all()
        for schedule in schedules:
            schedule.periodic_task.delete()
        return super(CustomerRDView, self).perform_destroy(instance)  # pylint: disable=no-member
