import os
from dotenv import load_dotenv
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

class EmailService:
    def __init__(self):
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = os.getenv("BREVO_API_KEY")
        
    async def send_email(self, recipient_email: str, subject: str, message: str) -> bool:
        try:
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
            
            sender = {"name": "Notification Service", "email": os.getenv("SENDER_EMAIL")}
            to = [{"email": recipient_email}]
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=to,
                html_content=message,
                sender=sender,
                subject=subject
            )
            
            api_response = api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Email envoyé avec succès à {recipient_email}")
            return True
                
        except ApiException as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {recipient_email}: {str(e)}")
            return False

# Instance globale du service email
email_service = EmailService()
