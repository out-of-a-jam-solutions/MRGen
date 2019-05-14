from rest_framework import generics

from reporter import models, serializers


class ReportLCView(generics.ListCreateAPIView):
    lookup_field = 'pk'
    serializer_class = serializers.ReportSerializer
    queryset = models.Report.objects.all()
