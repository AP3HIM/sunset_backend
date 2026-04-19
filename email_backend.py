import requests
from django.core.mail.backends.base import BaseEmailBackend

class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        api_key = "YOUR_BREVO_API_KEY"
        url = "https://api.brevo.com/v3/smtp/email"

        for message in email_messages:
            data = {
                "sender": {"email": "noreply@sunsetuploader.com", "name": "Sunset Uploader"},
                "to": [{"email": addr} for addr in message.to],
                "subject": message.subject,
                "htmlContent": message.body,
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": api_key,
            }
            try:
                requests.post(url, json=data, headers=headers, timeout=10)
            except Exception as e:
                print("Brevo send failed:", e)
        return len(email_messages)
