from django.urls import path

from .views import (
    ServiceRequestCreateView,
    MyRequestsView,
    AllRequestsView,
    UpdateRequestStatusView,
    AdminStatsView,
    RequestMessagesView,
)

urlpatterns = [

    path(
        "create/",
        ServiceRequestCreateView.as_view()
    ),

    path(
        "my/",
        MyRequestsView.as_view()
    ),

    path(
        "all/",
        AllRequestsView.as_view()
    ),

    path(
        "admin-stats/",
        AdminStatsView.as_view()
    ),

    path(
        "update-status/<int:request_id>/",
        UpdateRequestStatusView.as_view()
    ),

    path(
        "messages/<int:request_id>/",
        RequestMessagesView.as_view()
    ),
]