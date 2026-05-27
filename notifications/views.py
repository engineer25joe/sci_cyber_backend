from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer

from core.api_response import success, error


class MyNotificationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Notification.objects.filter(user=request.user).order_by("-created_at")
        return success(
            NotificationSerializer(notes, many=True).data,
            "Notifications fetched"
        )


class MarkAsReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            note = Notification.objects.get(id=notification_id, user=request.user)
            note.is_read = True
            note.save()

            return success(message="Marked as read")

        except Notification.DoesNotExist:
            return error("Notification not found", status=404)