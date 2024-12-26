import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from typing import Optional, Dict
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chargement des variables d'environnement
load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("EMAIL_FROM")

    async def send_email(self, recipient_email: str, subject: str, message: str, metadata: Optional[Dict] = None) -> bool:
        try:
            # Création du message
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject

            # Ajout du corps du message
            msg.attach(MIMEText(message, "plain"))

            # Connexion au serveur SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Activation du chiffrement TLS
                server.login(self.smtp_username, self.smtp_password)
                
                # Envoi de l'email
                server.send_message(msg)

            logger.info(f"Email envoyé avec succès à {recipient_email}")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email à {recipient_email}: {str(e)}")
            return False

# Instance globale du service email
email_service = EmailService()
