import os
from twilio.rest import Client
from typing import Dict

class SMSService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_FROM_NUMBER")
        self.client = Client(self.account_sid, self.auth_token)

    async def send_sms(self, to_number: str, message: str, metadata: Dict = None) -> bool:
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi du SMS: {str(e)}")
            return False
