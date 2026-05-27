from django.urls import path

from .views import (
    ServiceRequestCreateView,
    MyRequestsView,
)

urlpatterns = [

    path(
        "create/",
        ServiceRequestCreateView.as_view(),
    ),

    path(
        "my/",
        MyRequestsView.as_view(),
    ),
]