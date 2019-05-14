from rest_framework import serializers

from reporter import models


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Report
        fields = (
            'pk',
            'customer',
            'start_date',
            'end_date'
        )
