from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app import DEFAULT_CONFIG
from app.services.email_service import email_service
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Hospital Notification Service",
    description="Service de notification pour le système de localisation des patients",
    version="1.0.0"
)

class NotificationBase(BaseModel):
    recipient_id: str
    message: str
    notification_type: str  # 'email' ou 'sms'
    priority: str = DEFAULT_CONFIG["DEFAULT_PRIORITY"]  # 'normal' ou 'urgent'
    metadata: Optional[dict] = None

class NotificationResponse(BaseModel):
    recipient_id: str
    message: str
    notification_type: str
    priority: str
    metadata: Optional[dict]
    notification_id: str
    status: str
    timestamp: str

# Base fictive pour stocker les notifications
notifications_db = []

@app.get("/")
async def root():
    return {"message": "Notification Service is running"}

@app.post("/api/v1/notifications", response_model=NotificationResponse)
async def send_notification(notification: NotificationBase, background_tasks: BackgroundTasks):
    try:
        # Générer un ID unique pour la notification
        notification_id = f"notif_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Créer une notification avec la structure souhaitée
        notification_entry = {
            "recipient_id": notification.recipient_id,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "priority": notification.priority,
            "metadata": notification.metadata,
            "notification_id": notification_id,
            "status": "queued",
            "timestamp": datetime.now().isoformat()
        }
        
        # Ajouter la notification à la base fictive
        notifications_db.append(notification_entry)
        
        # Ajouter la tâche d'envoi à la file d'attente
        if notification.notification_type == "email":
            background_tasks.add_task(send_email_notification, notification)
        elif notification.notification_type == "sms":
            background_tasks.add_task(send_sms_notification, notification)
        else:
            raise HTTPException(status_code=400, detail="Type de notification non supporté")

        return NotificationResponse(
            recipient_id=notification.recipient_id,
            message=notification.message,
            notification_type=notification.notification_type,
            priority=notification.priority,
            metadata=notification.metadata,
            notification_id=notification_id,
            status="queued",
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_email_notification(notification: NotificationBase):
    try:
        # Construire le sujet de l'email
        subject = f"Notification {notification.priority} - {notification.metadata.get('department', '')}"
        
        # Utiliser le service email existant
        success = await email_service.send_email(
            recipient_email=notification.recipient_id,  # Assurez-vous que recipient_id est une adresse email
            subject=subject,
            message=notification.message,
            metadata=notification.metadata
        )
        
        # Mettre à jour le statut dans la base de données
        for notif in notifications_db:
            if notif["recipient_id"] == notification.recipient_id:
                notif["status"] = "sent" if success else "failed"
                
        return success
    except Exception as e:
        logger.error(f"Erreur d'envoi d'email: {str(e)}")
        return False

async def send_sms_notification(notification: NotificationBase):
    # TODO: Implémenter l'envoi de SMS
    pass

@app.get("/api/v1/notifications", response_model=List[NotificationResponse])
async def get_all_notifications():
    """
    Récupérer toutes les notifications enregistrées.
    """
    return [NotificationResponse(**notif) for notif in notifications_db]

@app.get("/api/v1/notifications/{notification_id}", response_model=NotificationResponse)
async def get_notification_status(notification_id: str):
    """
    Récupérer les détails d'une notification spécifique par ID.
    """
    # Rechercher la notification par ID dans la base fictive
    notification = next((notif for notif in notifications_db if notif["notification_id"] == notification_id), None)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification introuvable")
    return NotificationResponse(**notification)
