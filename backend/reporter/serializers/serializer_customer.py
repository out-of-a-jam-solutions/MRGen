from rest_framework import serializers

from backend.reporter import models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = (
            'pk',
            'name',
            'watchman_group_id',
            'repairshopr_id'
        )
