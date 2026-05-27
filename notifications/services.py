from .models import Notification
from .push_service import send_push_notification


def create_notification(user, title, message, type="system"):
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        type=type
    )

    # 🔔 PUSH TRIGGER
    send_push_notification(user, title, message)

    return notification