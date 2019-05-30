from knox.auth import TokenAuthentication
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from reporter import models, serializers


class ScheduleLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer
    queryset = models.ServiceSchedule.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('id', 'customer', 'task_type')


class ScheduleRDView(generics.RetrieveDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer
    queryset = models.ServiceSchedule.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        instance.periodic_task.delete()
        return super(ScheduleRDView, self).perform_destroy(instance)  # pylint: disable=no-member
