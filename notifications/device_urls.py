from django.urls import path
from .device_views import RegisterDeviceView

urlpatterns = [
    path("register-device/", RegisterDeviceView.as_view()),
]
