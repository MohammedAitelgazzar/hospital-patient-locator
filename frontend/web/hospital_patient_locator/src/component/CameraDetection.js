import React, { useRef, useEffect, useState } from 'react';
import './CameraDetection.css';

const CameraDetection = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [detectionResult, setDetectionResult] = useState(null);
  const [isActive, setIsActive] = useState(false);

  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: 'environment' } 
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing camera:", err);
      }
    };

    if (isActive) {
      startCamera();
    } else {
      // Stop the camera stream when isActive becomes false
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
        videoRef.current.srcObject = null;
      }
    }

    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, [isActive]);

  useEffect(() => {
    let interval;
    if (isActive) {
      interval = setInterval(captureFrame, 2000);
    }
    return () => clearInterval(interval);
  }, [isActive]);

  const captureFrame = async () => {
    if (!videoRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const video = videoRef.current;
    const context = canvas.getContext('2d');

    // Match canvas size to video dimensions
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw current video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Get base64 image data
    const imageData = canvas.toDataURL('image/jpeg');
    const base64Data = imageData.split(',')[1];

    try {
        const response = await fetch('http://localhost:5001/api/detection/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify({
                image: base64Data
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        setDetectionResult(result);
    } catch (error) {
        console.error('Error analyzing frame:', error);
    }
  };

  const handleStartCamera = () => {
    setIsActive(true);
  };

  const handleStopCamera = () => {
    setIsActive(false);
    setDetectionResult(null);
  };

  return (
    <div className="camera-container">
      <div className="camera-controls">
        <button 
          className={`control-button ${isActive ? 'stop' : 'start'}`}
          onClick={isActive ? handleStopCamera : handleStartCamera}
        >
          {isActive ? 'Stop Camera' : 'Start Camera'}
        </button>
      </div>
      
      <video
        ref={videoRef}
        autoPlay
        playsInline
        className="camera-feed"
      />
      <canvas
        ref={canvasRef}
        style={{ display: 'none' }}
      />
      {detectionResult && (
        <div className="detection-overlay">
          {detectionResult.data.detections.map((detection, index) => (
            <div 
              key={index}
              className="detection-box"
              style={{
                left: `${detection.box[0]}px`,
                top: `${detection.box[1]}px`,
                width: `${detection.box[2]}px`,
                height: `${detection.box[3]}px`,
              }}
            >
              <span className="detection-label">{detection.color}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CameraDetection;
