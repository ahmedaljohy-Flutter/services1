from rest_framework import serializers
from .models import Delivery

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'delv_name', 'description', 'delivered_by', 'created_at']
        read_only_fields = ['delivered_by']