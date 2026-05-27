import base64
import requests
from datetime import datetime


# ⚠️ REPLACE THESE WITH YOUR SAFARICOM DARAJA KEYS
CONSUMER_KEY = "YOUR_CONSUMER_KEY"
CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

BUSINESS_SHORTCODE = "174379"  # Sandbox test shortcode
PASSKEY = "YOUR_PASSKEY"

CALLBACK_URL = "https://your-domain.com/api/payments/callback/"


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    data = response.json()

    return data.get("access_token")


def generate_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = BUSINESS_SHORTCODE + PASSKEY + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode()).decode("utf-8")

    return encoded_string, timestamp


def stk_push(phone, amount):
    access_token = get_access_token()
    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "SCI_CYBER",
        "TransactionDesc": "Cyber Service Payment"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
