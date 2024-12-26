import React from 'react';
import './Signup.css';

const SignUp = () => {
  return (
    <div className="signup-container">
      <h1 className="signup-title">Sign Up</h1>
      <form>
        <div className="input-group">
          <label htmlFor="name">Name</label>
          <input type="text" id="name" placeholder="Enter your name" required />
        </div>
        <div className="input-group">
          <label htmlFor="email">E-mail</label>
          <input type="email" id="email" placeholder="Enter your email" required />
        </div>
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            placeholder="Enter your password"
            required
          />
        </div>
        <div className="form-footer">
          <button type="submit">Create Account</button>
          <p className="terms">
            By signing up, you agree to our <a href="#">Terms & Conditions</a>.
          </p>
        </div>
      </form>
      <p className="already-account">
        Already have an account? <a href="/">Login</a>
      </p>
    </div>
  );
};

export default SignUp;
