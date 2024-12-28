import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App"; // Login form
import SignUp from "./pages/Signup"; 
import reportWebVitals from './reportWebVitals';
import FloorMapComponent from "./component/FloorMapComponent";
import CameraDetection from "./component/CameraDetection";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/plan" element={<FloorMapComponent />} />
      <Route path="/camera" element={<CameraDetection />} />
    </Routes>
  </Router>
);


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

