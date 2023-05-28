from twilio.rest import Client

from app.core.config import settings


class TwilioService:
    def __init__(self):
        self.ACCOUNT_SID = settings.TWILIO_CONFIG.TWILIO_ACCOUNT_SID
        self.AUTH_TOKEN = settings.TWILIO_CONFIG.TWILIO_AUTH_TOKEN
        self.SENDER_PHONE_NUMBER = settings.TWILIO_CONFIG.TWILIO_SENDER_PHONE_NUMBER

        self.client = Client(self.ACCOUNT_SID, self.AUTH_TOKEN)

    def send_verification_message(self, phone_number: str, message: str) -> bool:
        message = self.client.messages.create(
            from_=self.SENDER_PHONE_NUMBER, to=phone_number, body=message
        )

        return True