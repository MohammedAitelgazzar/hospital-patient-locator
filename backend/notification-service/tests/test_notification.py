import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Notification Service is running"}

def test_send_email_notification():
    notification_data = {
        "recipient_id": "test@example.com",
        "message": "Test notification",
        "notification_type": "email",
        "priority": "normal",
        "metadata": {"department": "cardiology"}
    }
    response = client.post("/api/v1/notifications", json=notification_data)
    assert response.status_code == 200
    assert "notification_id" in response.json()
    assert response.json()["status"] == "queued"

def test_send_sms_notification():
    notification_data = {
        "recipient_id": "+33612345678",
        "message": "Test SMS notification",
        "notification_type": "sms",
        "priority": "urgent",
        "metadata": {"type": "emergency"}
    }
    response = client.post("/api/v1/notifications", json=notification_data)
    assert response.status_code == 200
    assert "notification_id" in response.json()
    assert response.json()["status"] == "queued"
