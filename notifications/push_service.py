import requests
from .device_models import Device


# 🔥 FUTURE FCM HOOK (ready for Firebase)
FCM_URL = "https://fcm.googleapis.com/fcm/send"
FCM_SERVER_KEY = "YOUR_FIREBASE_SERVER_KEY"


def send_push_notification(user, title, message):
    devices = Device.objects.filter(user=user, is_active=True)

    tokens = [d.device_token for d in devices]

    if not tokens:
        return {"status": "no_devices"}

    payload = {
        "registration_ids": tokens,
        "notification": {
            "title": title,
            "body": message
        }
    }

    headers = {
        "Authorization": f"key={FCM_SERVER_KEY}",
        "Content-Type": "application/json"
    }

    # ⚠️ In MVP we simulate success (you can activate later)
    try:
        response = requests.post(FCM_URL, json=payload, headers=headers)
        return response.json()
    except:
        return {"status": "failed", "reason": "push service offline"}
