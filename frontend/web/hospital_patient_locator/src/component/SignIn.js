import React from 'react';
import { Link } from 'react-router-dom';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import '../style/Signin.css'; 

const SignIn = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });
  const navigate = useNavigate(); // Hook for navigation

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();  // Prevent default form submission behavior
    navigate('./FloorMapComponent'); // Navigate to FloorMapComponent
  };

  return (
    <div className="signin-signup-page">
    <div className="login-container">
      <div className="login-card">
        <div className="login-image">
          <img src={require("../assets/hospitallogin.png")} alt="Medical Illustration" />
        </div>
        <div className="login-form">
          <h2 className="form-title">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="username">Username</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                placeholder="Enter your username"
                required
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Enter your password"
                required
              />
            </div>
            
            <button type="submit" className="login-button">Login</button>
          </form>
          <p className="form-footer">
            Don’t have an account? <Link to="/signup">Sign up</Link>
          </p>
        </div>
      </div>
    </div>
</div>
  );
};

export default SignIn;
