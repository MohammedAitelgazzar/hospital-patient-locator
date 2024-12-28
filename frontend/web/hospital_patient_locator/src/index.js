import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
<<<<<<< HEAD
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css';
import 'leaflet-defaulticon-compatibility';
import { BrowserRouter } from 'react-router-dom';  // Import BrowserRouter
=======
import FloorMapComponent from "./component/FloorMapComponent";
import CameraDetection from "./component/CameraDetection";
>>>>>>> 1bf2644cb12b230da951345c768947ff95ac64e7

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
<<<<<<< HEAD
  <React.StrictMode>
    <BrowserRouter>  {/* Wrap your App component with BrowserRouter */}
      <App />
    </BrowserRouter>
  </React.StrictMode>
=======
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/plan" element={<FloorMapComponent />} />
      <Route path="/camera" element={<CameraDetection />} />
    </Routes>
  </Router>
>>>>>>> 1bf2644cb12b230da951345c768947ff95ac64e7
);

reportWebVitals();

