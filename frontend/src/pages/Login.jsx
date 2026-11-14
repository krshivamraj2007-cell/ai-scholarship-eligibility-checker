
import React, { useState } from "react";
import "./Login.css";

function Login({ onBack, onRegister, onLoginSuccess }) {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

    // Store JWT token
    localStorage.setItem("access_token", data.access_token);

    // Store user information
    localStorage.setItem("user", JSON.stringify(data.user));

    // Notify App.jsx about successful login
    onLoginSuccess(data.user);

    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">

      <button
        type="button"
        onClick={onBack}
        className="back-btn"
      >
        ← Back to Home
      </button>

      <h1>Welcome Back to ScholarAI</h1>

      <p>Login to explore scholarships and government schemes.</p>

      <form onSubmit={handleSubmit}>

        <input
          type="email"
          name="email"
          placeholder="Email Address"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        {message && <p>{message}</p>}

      </form>

      <p>
        Don't have an account?{" "}
        <button type="button" onClick={onRegister}>
          Create Account
        </button>
      </p>

    </div>
  );
}

export default Login;
