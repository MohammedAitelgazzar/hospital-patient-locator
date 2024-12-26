# Version de l'application
__version__ = "1.0.0"

# Configuration de base
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

DEFAULT_CONFIG = {
    "EMAIL_ENABLED": os.getenv("EMAIL_ENABLED", "true").lower() == "true",
    "SMS_ENABLED": os.getenv("SMS_ENABLED", "true").lower() == "true",
    "DEFAULT_PRIORITY": "normal"
}
