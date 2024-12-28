import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import '../style/Signup.css'; 

const SignUp = () => {
  const [formData, setFormData] = useState({
    name: "",
    username: "",
    password: "",
    role: "PATIENT",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Sign Up Data: ", formData);
  };

  return (
    <div className="signup-container">
      <div className="signup-card">
      <div className="login-image">
          <img src={require("../assets/hospitallogin.png")} alt="Medical Illustration" />
        </div>
        <h2 className="form-title">Sign Up</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="name">Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter your name"
              required
            />
          </div>
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
          <div className="input-group">
            <label htmlFor="role">Role</label>
            <select
              id="role"
              name="role"
              value={formData.role}
              onChange={handleChange}
            >
              <option value="DOCTEUR">Docteur</option>
              <option value="PATIENT">Patient</option>
            </select>
          </div>
          <button type="submit" className="signup-button">Sign Up</button>
        </form>
        <p className="form-footer">
          Already have an account? <Link to="/">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default SignUp;
