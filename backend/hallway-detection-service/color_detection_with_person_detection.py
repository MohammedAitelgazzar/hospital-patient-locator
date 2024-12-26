import cv2
import numpy as np
import requests  # Import the requests library
import logging  # Import the logging module

# Configure logging
logging.basicConfig(
    filename='detection_log.txt',  # Log file name
    level=logging.INFO,  # Log level
    format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
)

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

print("Unconnected Out Layers:", output_layers)  # Debug print

# Function to detect colors
def detect_color(frame):
    if frame is None or frame.size == 0:  # Check if the frame is empty
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

# Function to send notification to an API
def send_notification(color_label):
    url = "https://your-api-endpoint.com/notify"  # Replace with your API endpoint
    data = {
        "message": f"Detected a person wearing {color_label}."
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Notification sent successfully.")
        else:
            print("Failed to send notification:", response.status_code, response.text)
    except Exception as e:
        print("Error sending notification:", str(e))

# Start video capture
cap = cv2.VideoCapture(0)

# Set to track detected persons
detected_persons = []

# Define a threshold for distance to consider the same person
DISTANCE_THRESHOLD = 50  # Adjust this value as needed

while True:
    ret, frame = cap.read()
    if not ret or frame is None or frame.size == 0:  # Check if frame is valid
        print("Failed to capture frame")  # Debug message
        break

    # Detecting persons
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes = []
    confidences = []
    class_ids = []

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

                # Create bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    if len(indices) > 0:
        for i in indices.flatten():  # Use flatten() to get a 1D array
            box = boxes[i]
            x, y, w, h = box

            # Calculate the center of the bounding box
            center_x = x + w // 2
            center_y = y + h // 2

            # Check if this person has already been detected
            person_detected = False
            for detected in detected_persons:
                # Calculate the distance between the current and detected person
                distance = np.sqrt((center_x - detected[0]) ** 2 + (center_y - detected[1]) ** 2)
                if distance < DISTANCE_THRESHOLD:
                    person_detected = True
                    break

            if not person_detected:
                # Add the new detected person to the list
                detected_persons.append((center_x, center_y))

                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Crop the detected person
                person_roi = frame[y:y + h, x:x + w]

                # Detect color in the cropped region
                color_label = detect_color(person_roi)

                # Log the detected color
                logging.info(f"Detected: {color_label} at coordinates: ({x}, {y}, {w}, {h})")

                # Display the color label
                cv2.putText(frame, color_label, (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Send notification if wearing blue or green
                if color_label in ["Wearing Blue", "Wearing Green"]:
                    send_notification(color_label)

    cv2.imshow('Video Feed', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 