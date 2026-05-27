from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import IsAdmin
from .analytics import get_admin_dashboard_stats


class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        data = get_admin_dashboard_stats()
        return Response(data)
