from django.db import models
from django.conf import settings
from services.models import Service


class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ("pending_payment", "Pending Payment"),
        ("paid", "Paid"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("waiting_review", "Waiting Review"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    description = models.TextField()

    attached_file = models.FileField(
      upload_to="service_requests/%Y/%m/%d/",
      null=True,
      blank=True
    )

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending_payment")

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_jobs"
    )

    estimated_completion_time = models.DateTimeField(null=True, blank=True)

    ai_used = models.BooleanField(default=False)

    price_charged = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"