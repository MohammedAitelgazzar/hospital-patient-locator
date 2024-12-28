from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import py_eureka_client.eureka_client as eureka_client
import logging
import os
from dotenv import load_dotenv
import cv2
import numpy as np
from typing import Optional, List
import base64
import urllib.request

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app configuration
app = FastAPI(
    title="Hallway Detection Service",
    description="Service for detecting hallways and processing images",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Eureka configuration
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")
APP_NAME = os.getenv("APP_NAME", "HALLWAY-DETECTION-SERVICE")
PORT = int(os.getenv("PORT", "5001"))
INSTANCE_HOST = os.getenv("INSTANCE_HOST", "localhost")

# Update the path to YOLO files
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
YOLO_CONFIG = os.path.join(MODELS_DIR, "yolov3.cfg")
YOLO_WEIGHTS = os.path.join(MODELS_DIR, "yolov3.weights")

# Create models directory if it doesn't exist
os.makedirs(MODELS_DIR, exist_ok=True)

def download_yolo_files():
    if not os.path.exists(YOLO_CONFIG):
        logger.info("Downloading YOLOv3 config file...")
        cfg_url = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg"
        urllib.request.urlretrieve(cfg_url, YOLO_CONFIG)
    
    if not os.path.exists(YOLO_WEIGHTS):
        logger.info("Downloading YOLOv3 weights file (this may take a while)...")
        weights_url = "https://pjreddie.com/media/files/yolov3.weights"
        urllib.request.urlretrieve(weights_url, YOLO_WEIGHTS)

# Initialize YOLO
try:
    if not os.path.exists(YOLO_CONFIG) or not os.path.exists(YOLO_WEIGHTS):
        logger.info("YOLO files not found. Attempting to download...")
        download_yolo_files()
        
    net = cv2.dnn.readNet(YOLO_WEIGHTS, YOLO_CONFIG)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    logger.info("YOLO model loaded successfully")
except Exception as e:
    logger.error(f"Error loading YOLO model: {e}")
    net = None
    output_layers = None

# Color detection function
def detect_color(frame):
    if frame is None or frame.size == 0:
        return "No Frame"

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges for blue
    blue_lower = np.array([100, 150, 0])
    blue_upper = np.array([140, 255, 255])
    
    # Define color ranges for green
    green_lower = np.array([40, 100, 0])
    green_upper = np.array([80, 255, 255])

    # Create masks for blue and green
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    if cv2.countNonZero(blue_mask) > 0:
        return "Wearing Blue"
    elif cv2.countNonZero(green_mask) > 0:
        return "Wearing Green"
    else:
        return "Unknown"

# Person detection function
def detect_persons(frame):
    if net is None or output_layers is None:
        logger.error("YOLO model not initialized")
        return []

    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []
    detections = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and class_id == 0:  # Class ID 0 is for 'person'
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            person_roi = frame[y:y+h, x:x+w]
            color = detect_color(person_roi)
            detections.append({
                "box": [x, y, w, h],
                "color": color,
                "confidence": confidences[i]
            })

    return detections

# Eureka client initialization
eureka_client_instance = None

@app.on_event("startup")
async def startup_event():
    global eureka_client_instance
    try:
        eureka_client_instance = await eureka_client.init_async(
            eureka_server=EUREKA_SERVER,
            app_name=APP_NAME,
            instance_port=PORT,
            instance_host=INSTANCE_HOST,
            status_page_url=f"http://{INSTANCE_HOST}:{PORT}/info",
            health_check_url=f"http://{INSTANCE_HOST}:{PORT}/health"
        )
        logger.info(f"Successfully registered with Eureka server at {EUREKA_SERVER}")
    except Exception as e:
        logger.error(f"Failed to register with Eureka server: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    global eureka_client_instance
    try:
        if eureka_client_instance:
            await eureka_client_instance.stop()
            logger.info("Successfully deregistered from Eureka server")
    except Exception as e:
        logger.error(f"Error deregistering from Eureka: {e}")

class ImageData(BaseModel):
    image: str  # Base64 encoded image
    metadata: Optional[dict] = None

@app.post("/api/detection/analyze")
async def analyze_image(data: ImageData):
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(data.image)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail="Invalid image data")

        # Perform detection
        detections = detect_persons(frame)

        return {
            "status": "success",
            "data": {
                "detections": detections,
                "total_persons": len(detections)
            }
        }
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "UP"}

@app.get("/info")
async def info():
    return {
        "app_name": APP_NAME,
        "version": "1.0.0",
        "status": "Running"
    }

@app.get("/")
async def root():
    return {"message": "Hallway Detection Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)