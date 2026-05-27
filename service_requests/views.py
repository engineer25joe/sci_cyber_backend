from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from rest_framework import status

from .models import ServiceRequest

from services.models import Service


class ServiceRequestCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        print("AUTH USER:", request.user)

        service_id = request.data.get("service")

        description = request.data.get("description")

        if not service_id or not description:

            return Response(
                {
                    "error": "Service and description are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            service = Service.objects.get(id=service_id)

        except Service.DoesNotExist:

            return Response(
                {
                    "error": "Service not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        service_request = ServiceRequest.objects.create(
            user=request.user,
            service=service,
            description=description,
        )

        return Response(
            {
                "message": "Request submitted successfully",
                "id": service_request.id,
                "service": service.title,
                "description": service_request.description,
                "status": service_request.status,
            },
            status=status.HTTP_201_CREATED
        )


class MyRequestsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        print("FETCHING REQUESTS FOR:", request.user)

        requests = ServiceRequest.objects.filter(
            user=request.user
        ).order_by("-created_at")

        data = []

        for item in requests:

            data.append({
                "id": item.id,
                "service_name": item.service.title,
                "description": item.description,
                "status": item.status,
                "created_at": item.created_at,
            })

        return Response(data)