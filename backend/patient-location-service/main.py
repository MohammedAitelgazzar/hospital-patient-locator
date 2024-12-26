from flask import Flask, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import base64
import logging
import json

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

# Mock user data - in a real app this would come from a database
MOCK_USER = {
    "id": "12345",
    "name": "John Doe",
    "age": 45,
    "room": "B-203",
    "condition": "Stable",
    "admission_date": "2024-03-15"
}

@app.route('/scan', methods=['POST'])
def scan_qr_code():
    try:
        # Get the image data from the request
        data = request.json
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data received'}), 400

        # Log incoming request details
        logging.debug(f"Processing image data...")

        # Convert base64 image to numpy array
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        
        # Convert YUV420 to grayscale
        width = int(data.get('width', 0))
        height = int(data.get('height', 0))
        
        if width and height:
            # Reshape considering the YUV420 format
            y_plane = nparr[:width*height].reshape(height, width)
            
            # Enhanced image processing pipeline
            # 1. Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(y_plane, (5, 5), 0)
            
            # 2. Apply adaptive thresholding with better parameters
            binary = cv2.adaptiveThreshold(
                blurred, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )
            
            # 3. Apply morphological operations to clean up the image
            kernel = np.ones((3,3), np.uint8)
            morphed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # 4. Try to detect QR codes in both the binary and morphed images
            decoded_objects = decode(binary) or decode(morphed)
            
            if not decoded_objects:
                # 5. If no QR code found, try with the original image
                decoded_objects = decode(y_plane)
        else:
            return jsonify({'error': 'Invalid image dimensions'}), 400

        # If QR codes are found, return their data with user info
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                qr_data = obj.data.decode('utf-8')
                # Here we're just using the mock user, but in a real app
                # you would look up the user based on the QR code data
                results.append({
                    'qr_data': qr_data,
                    'type': obj.type,
                    'user': MOCK_USER
                })
            logging.debug(f"QR Code detected with user info: {results}")
            return jsonify({'success': True, 'results': results})
        
        return jsonify({'success': False, 'message': 'No QR code detected'})

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
