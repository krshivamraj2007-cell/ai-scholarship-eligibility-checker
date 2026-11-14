
import React from "react";

function Dashboard({ user, onLogout }) {
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

          <div className="dashboard-card">
            <h2>🏛️</h2>
            <h3>Government Schemes</h3>
            <p>Explore financial assistance programs.</p>
          </div>

          <div className="dashboard-card">
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
