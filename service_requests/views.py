from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser
)

from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)

from django.contrib.auth import get_user_model

from .models import (
    ServiceRequest,
    RequestMessage
)

from services.models import Service

User = get_user_model()


class ServiceRequestCreateView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def post(self, request):

        try:

            service_id = request.data.get(
                "service"
            )

            description = request.data.get(
                "description"
            )

            attached_file = request.FILES.get(
                "attached_file"
            )

            service = Service.objects.get(
                id=service_id
            )

            service_request = (
                ServiceRequest.objects.create(
                    user=request.user,
                    service=service,
                    description=description,
                    attached_file=attached_file
                )
            )

            return Response({
                "message":
                "Request submitted successfully",

                "id": service_request.id
            })

        except Exception as e:

            return Response({
                "error": str(e)
            }, status=400)


class MyRequestsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        requests = (
            ServiceRequest.objects
            .filter(user=request.user)
            .order_by("-created_at")
        )

        data = []

        for item in requests:

            data.append({

                "id": item.id,

                "description":
                item.description,

                "status":
                item.status,

                "created_at":
                item.created_at,

                "service": {
                    "id":
                    item.service.id,

                    "title":
                    item.service.title
                }
            })

        return Response(data)


class AllRequestsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        requests = (
            ServiceRequest.objects
            .all()
            .order_by("-created_at")
        )

        data = []

        for item in requests:

            data.append({

                "id": item.id,

                "description":
                item.description,

                "status":
                item.status,

                "created_at":
                item.created_at,

                "user": {
                    "id":
                    item.user.id,

                    "username":
                    item.user.username
                },

                "service": {
                    "id":
                    item.service.id,

                    "title":
                    item.service.title
                }
            })

        return Response(data)


class UpdateRequestStatusView(APIView):

    permission_classes = [IsAdminUser]

    def post(
        self,
        request,
        request_id
    ):

        try:

            status = request.data.get(
                "status"
            )

            service_request = (
                ServiceRequest.objects.get(
                    id=request_id
                )
            )

            service_request.status = status

            service_request.save()

            return Response({
                "message":
                "Status updated successfully"
            })

        except Exception as e:

            return Response({
                "error": str(e)
            }, status=400)


class AdminStatsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        return Response({

            "total_requests":
            ServiceRequest.objects.count(),

            "completed_requests":
            ServiceRequest.objects.filter(
                status="completed"
            ).count(),

            "pending_requests":
            ServiceRequest.objects.filter(
                status="pending_payment"
            ).count(),

            "rejected_requests":
            ServiceRequest.objects.filter(
                status="rejected"
            ).count(),

            "total_users":
            User.objects.count(),
        })


class RequestMessagesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
        request_id
    ):

        messages = (
            RequestMessage.objects
            .filter(request_id=request_id)
            .order_by("created_at")
        )

        data = []

        for item in messages:

            data.append({

                "id": item.id,

                "message":
                item.message,

                "sender":
                item.sender.username,

                "sender_id":
                item.sender.id,

                "created_at":
                item.created_at
            })

        return Response(data)

    def post(
        self,
        request,
        request_id
    ):

        try:

            message = request.data.get(
                "message"
            )

            service_request = (
                ServiceRequest.objects.get(
                    id=request_id
                )
            )

            new_message = (
                RequestMessage.objects.create(
                    request=service_request,
                    sender=request.user,
                    message=message
                )
            )

            return Response({
                "id": new_message.id,

                "message":
                new_message.message,

                "sender":
                new_message.sender.username
            })

        except Exception as e:

            return Response({
                "error": str(e)
            }, status=400)