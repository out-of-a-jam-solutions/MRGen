from rest_framework import generics

from reporter import models, serializers


class ScheduleLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer
    queryset = models.ServiceSchedule.objects.all()
    filterset_fields = ('id', 'customer', 'task_type')


class ScheduleRDView(generics.RetrieveDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer
    queryset = models.ServiceSchedule.objects.all()

    def perform_destroy(self, instance):
        instance.periodic_task.delete()
        return super(ScheduleRDView, self).perform_destroy(instance)  # pylint: disable=no-member
