from django.db.models import Count, Sum
from service_requests.models import ServiceRequest
from payments.models import Payment
from accounts.models import User
from services.models import Service


def get_admin_dashboard_stats():
    return {
        "total_users": User.objects.count(),
        "total_customers": User.objects.filter(role="customer").count(),
        "total_attendants": User.objects.filter(role="attendant").count(),

        "total_services": Service.objects.count(),
        "published_services": Service.objects.filter(status="published").count(),

        "total_requests": ServiceRequest.objects.count(),
        "completed_requests": ServiceRequest.objects.filter(status="completed").count(),
        "pending_requests": ServiceRequest.objects.filter(status="pending_payment").count(),

        "total_revenue": Payment.objects.filter(status="completed").aggregate(
            total=Sum("amount")
        )["total"] or 0,
    }
