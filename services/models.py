from django.db import models
from django.conf import settings


class Service(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("pending_approval", "Pending Approval"),
        ("published", "Published"),
        ("rejected", "Rejected"),
    )

    PRICING_TYPE = (
        ("fixed", "Fixed"),
        ("dynamic", "Dynamic"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPE, default="fixed")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    estimated_time_minutes = models.IntegerField(default=0)

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="draft")

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="services_created"
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="services_approved"
    )

    is_ai_supported = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title