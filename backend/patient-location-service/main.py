from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import base64
import logging
import json
import py_eureka_client.eureka_client as eureka_client
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Eureka configuration
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")
APP_NAME = os.getenv("APP_NAME", "PATIENT-LOCATION-SERVICE")
PORT = int(os.getenv("PORT", "5002"))
INSTANCE_HOST = os.getenv("INSTANCE_HOST", "localhost")

# Initialize eureka client
def register_with_eureka():
    try:
        eureka_client.init(
            eureka_server=EUREKA_SERVER,
            app_name=APP_NAME,
            instance_port=PORT,
            instance_host=INSTANCE_HOST
        )
        logger.info(f"Successfully registered with Eureka server at {EUREKA_SERVER}")
    except Exception as e:
        logger.error(f"Failed to register with Eureka server: {e}")
        raise

# Register with Eureka on startup
register_with_eureka()

# Add health check endpoint for Eureka
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "UP"})

# Add info endpoint for Eureka
@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app_name": APP_NAME,
        "version": "1.0.0",
        "status": "Running"
    })

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    try:
        # Get the image data from the request
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data received'}), 400
        
        logging.debug(f"Processing image data...")

        # Convert base64 image to numpy array
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        width = int(data.get('width', 0))
        height = int(data.get('height', 0))
        
        if width and height:
            y_plane = nparr[:width*height].reshape(height, width)
            
            # Apply image processing steps
            blurred = cv2.GaussianBlur(y_plane, (5, 5), 0)
            binary = cv2.adaptiveThreshold(
                blurred, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            
            kernel = np.ones((3,3), np.uint8)
            morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            decoded_objects = decode(binary) or decode(morphed) or decode(y_plane)
        else:
            return jsonify({'error': 'Invalid image dimensions'}), 400

        if decoded_objects:
            results = []
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                results.append({
                    'qr_data': qr_data,
                    'type': obj.type
                })
            return jsonify({'success': True, 'results': results})
        
        return jsonify({'success': False, 'message': 'No QR code detected'})

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
