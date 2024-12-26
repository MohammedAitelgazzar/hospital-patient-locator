import React from "react";
import { Link } from "react-router-dom";
import "./App.css";

const App = () => {
  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-image">
          <img src={require("./assets/hospitallogin.png")} alt="Medical Illustration" />
        </div>
        <div className="login-form">
          <h2 className="form-title">Login</h2>
          <form>
            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input type="text" id="username" placeholder="Enter your username" />
            </div>
            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input type="password" id="password" placeholder="Enter your password" />
            </div>
            <button type="submit" className="login-button">Login</button>
          </form>
          <p className="form-footer">
            Don’t have an account? <Link to="/signup">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
