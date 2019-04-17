from rest_framework import generics

from reporter import models
from reporter import serializers


class ScheduleLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        return models.Schedule.objects.all()


class ScheduleRDView(generics.RetrieveDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ScheduleSerializer

    def get_queryset(self):
        return models.Schedule.objects.all()
