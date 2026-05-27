from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import PaymentSerializer
from .daraja import stk_push

from core.api_response import success, error


class InitiatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            payment = serializer.save(user=request.user)

            response = stk_push(payment.phone_number, payment.amount)

            return success({
                "payment": PaymentSerializer(payment).data,
                "daraja": response
            }, "STK push sent")

        return error("Payment failed", data=serializer.errors)


class MyPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user)
        return success(
            PaymentSerializer(payments, many=True).data,
            "Payments fetched"
        )