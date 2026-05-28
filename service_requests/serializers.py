from rest_framework import serializers
from .models import ServiceRequest
from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceRequest
        fields = [
            "id",
            "service",
            "description",
            "status",
            "price_charged",
            "is_paid",
            "created_at",
            "updated_at",
            "estimated_completion_time",
            "ai_used",
        ]