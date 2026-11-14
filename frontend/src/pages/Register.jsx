
import "./Register.css";

import React, { useState } from "react";

function Register( { onBack } ) {
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const [message, setMessage] = useState("");
const [loading, setLoading] = useState(false);

const handleSubmit = async (e) => {
  e.preventDefault();

  if (formData.password !== formData.confirmPassword) {
    setMessage("Passwords do not match!");
    return;
  }

  setLoading(true);
  setMessage("");

  try {
    const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        full_name: formData.fullName,
        email: formData.email,
        password: formData.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Registration failed");
    }

    setMessage("Account created successfully!");

    setFormData({
      fullName: "",
      email: "",
      password: "",
      confirmPassword: "",
    });

  } catch (error) {
    setMessage(error.message);
  } finally {
    setLoading(false);
  }
};
  return (
    <div className="register-container">
        <button
            type="button"
            onClick={onBack}
            className="back-btn"
        >
            ← Back to Home
        </button>
      <h1>Create Your ScholarAI Account</h1>
      <p>Register to discover scholarships and government schemes.</p>

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="fullName"
          placeholder="Full Name"
          value={formData.fullName}
          onChange={handleChange}
          required
        />

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

        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Creating Account..." : "Create Account"}
        </button>

        {message && <p>{message}</p>}
      </form>
    </div>
  );
}

export default Register;
