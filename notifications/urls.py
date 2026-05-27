from django.urls import path
from .views import MyNotificationsView, MarkAsReadView

urlpatterns = [
    path("my/", MyNotificationsView.as_view()),
    path("read/<int:notification_id>/", MarkAsReadView.as_view()),
]
