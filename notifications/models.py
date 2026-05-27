from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = (
        ("payment", "Payment"),
        ("job", "Job"),
        ("system", "System"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    message = models.TextField()

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="system")

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title