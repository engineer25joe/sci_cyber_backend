from django.urls import path
from .views import InitiatePaymentView, MyPaymentsView
from .callback import MpesaCallbackView

urlpatterns = [
    path("initiate/", InitiatePaymentView.as_view()),
    path("my/", MyPaymentsView.as_view()),
    path("callback/", MpesaCallbackView.as_view()),
]