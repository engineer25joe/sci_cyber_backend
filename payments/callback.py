from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment


class MpesaCallbackView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        try:
            result = data["Body"]["stkCallback"]

            receipt = None
            amount = None
            phone = None

            if result["ResultCode"] == 0:
                items = result["CallbackMetadata"]["Item"]

                for item in items:
                    if item["Name"] == "MpesaReceiptNumber":
                        receipt = item["Value"]
                    if item["Name"] == "Amount":
                        amount = item["Value"]
                    if item["Name"] == "PhoneNumber":
                        phone = item["Value"]

                payment = Payment.objects.filter(phone_number=phone, amount=amount).last()

                if payment:
                    payment.status = "completed"
                    payment.mpesa_receipt = receipt
                    payment.save()

            return Response({"Result": "OK"})

        except Exception as e:
            return Response({"error": str(e)})
