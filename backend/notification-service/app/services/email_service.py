import os
import requests
from dotenv import load_dotenv
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

class EmailService:
    def __init__(self):
        self.mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        self.mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        self.mailgun_base_url = "https://api.eu.mailgun.net/v3"

    async def send_email(self, recipient_email: str, subject: str, message: str) -> bool:
        try:
            response = requests.post(
                f"{self.mailgun_base_url}/{self.mailgun_domain}/messages",
                auth=("api", self.mailgun_api_key),
                data={
                    "from": f"Notification Service <mailgun@{self.mailgun_domain}>",
                    "to": [recipient_email],
                    "subject": subject,
                    "text": message,
                    "html": message
                }
            )
            
            if response.status_code == 200:
                logger.info(f"Email envoyé avec succès à {recipient_email}")
                return True
            else:
                logger.error(f"Erreur lors de l'envoi de l'email: {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {recipient_email}: {str(e)}")
            return False

# Instance globale du service email
email_service = EmailService()
