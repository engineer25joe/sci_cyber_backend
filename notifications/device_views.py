from rest_framework.views import APIView
from rest_framework.response import Response

from .device_models import Device
from .device_serializers import DeviceSerializer


class RegisterDeviceView(APIView):
    def post(self, request):
        serializer = DeviceSerializer(data=request.data)

        if serializer.is_valid():
            device, created = Device.objects.update_or_create(
                device_token=serializer.validated_data["device_token"],
                defaults={
                    "user": request.user,
                    "platform": serializer.validated_data["platform"],
                    "is_active": True
                }
            )

            return Response(DeviceSerializer(device).data)

        return Response(serializer.errors, status=400)
