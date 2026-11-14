import GovernmentSchemes from "./GovernmentSchemes";
import StudentProfile from "./StudentProfile";
import React, { useState } from "react";
import "./Dashboard.css";

function Dashboard({ user, onLogout }) {
  const [showProfile, setShowProfile] = useState(false);
  const [showSchemes, setShowSchemes] = useState(false);
  if (showProfile) {
  return (
    <StudentProfile
      user={user}
      onBack={() => setShowProfile(false)}
    />
  );
}
  if (showSchemes) {
  return (
    <GovernmentSchemes
      onBack={() => setShowSchemes(false)}
    />
  );
}
  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="logo">
          Scholar<span>AI</span>
        </div>

        <button className="login-btn" onClick={onLogout}>
          Logout
        </button>
      </nav>

      <div className="dashboard-content">
        <h1>Welcome, {user?.full_name || "Student"}! 👋</h1>

        <p>
          Your ScholarAI journey starts here.
        </p>

        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h2>🎓</h2>
            <h3>Find Scholarships</h3>
            <p>Discover scholarships matching your profile.</p>
          </div>

          <div
            className="dashboard-card"
            onClick={() => setShowSchemes(true)}
            style={{ cursor: "pointer" }}
          >
            <h2>🏛️</h2>
            <h3>Government Schemes</h3>
            <p>Explore financial assistance programs.</p>
          </div>
          <div
            className="dashboard-card"
            onClick={() => setShowProfile(true)}
            style={{ cursor: "pointer" }}
          >
            <h2>👤</h2>
            <h3>My Profile</h3>
            <p>Manage your student information.</p>
          </div>

          <div className="dashboard-card">
            <h2>🤖</h2>
            <h3>AI Assistant</h3>
            <p>Get scholarship eligibility guidance.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
