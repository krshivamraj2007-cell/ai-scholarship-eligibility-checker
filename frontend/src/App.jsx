import AIChat from "./components/AIChat";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [backendStatus, setBackendStatus] = useState("Checking...");
  const [showRegister, setShowRegister] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
  const [currentUser, setCurrentUser] = useState(
  JSON.parse(localStorage.getItem("user") || "null")
);

const [isLoggedIn, setIsLoggedIn] = useState(
  Boolean(localStorage.getItem("access_token"))
);
  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => {
        if (!response.ok) throw new Error("Backend unavailable");
        return response.json();
      })
      .then(() => setBackendStatus("Online"))
      .catch(() => setBackendStatus("Offline"));
  }, []);
    if (isLoggedIn) {
    return (
      <Dashboard
        user={currentUser}
        onLogout={() => {
          localStorage.removeItem("access_token");
          localStorage.removeItem("user");
          setCurrentUser(null);
          setIsLoggedIn(false);
        }}
      />
    );
  }
    if (showRegister) {
    return (
      <Register
        onBack={() => setShowRegister(false)}
      />
    );
      
}

  if (showLogin) {
  return (
    <Login
      onBack={() => setShowLogin(false)}
      onRegister={() => {
        setShowLogin(false);
        setShowRegister(true);
      }}
      onLoginSuccess={(user) => {
        setCurrentUser(user);
        setIsLoggedIn(true);
        setShowLogin(false);
      }}
    />
  );
}

  return (
    <div className="app">

      {/* Navigation */}
      <nav className="navbar">
        <div className="logo">
          Scholar<span>AI</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
        </div>

        <button
          className="login-btn"
          onClick={() => setShowLogin(true)}
        >
          Login
        </button>
      </nav>

      {/* Hero Section */}
      <section className="hero" id="home">
        <div className="hero-content">

          <span className="tagline">
            AI POWERED SCHOLARSHIP PLATFORM
          </span>

          <h1>
            Find Scholarships
            <br />
            You're <span>Eligible For.</span>
          </h1>

          <p>
            Discover scholarships and government schemes
            that match your profile. Let AI help you find
            the right financial opportunities for your education.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn"
                    onClick={() => setShowRegister(true)}
            >
                    Get Started →
            </button>

            <button className="secondary-btn">
              Explore Scholarships
            </button>
          </div>

          <div className="trust-text">
            Your education deserves every opportunity.
          </div>
        </div>

        <div className="hero-card">
          <div className="card-icon">🎓</div>
          <h2>Scholarship Finder</h2>
          <p>Smart recommendations powered by AI</p>

          <div className="mini-feature">
            <span>✓</span> Personalized matching
          </div>

          <div className="mini-feature">
            <span>✓</span> Eligibility analysis
          </div>

          <div className="mini-feature">
            <span>✓</span> Application guidance
          </div>
        </div>
      </section>

      {/* Statistics */}
      <section className="stats">
        <div>
          <h2>AI</h2>
          <p>Smart Matching</p>
        </div>

        <div>
          <h2>24/7</h2>
          <p>AI Assistance</p>
        </div>

        <div>
          <h2>100%</h2>
          <p>Student Focused</p>
        </div>
      </section>

      {/* Features */}
      <section className="features" id="features">
        <div className="section-heading">
          <span>OUR FEATURES</span>
          <h2>Everything You Need in One Place</h2>
          <p>Discover opportunities and simplify your scholarship journey.</p>
        </div>

        <div className="feature-grid">
          <div className="feature-card">
            <div>🤖</div>
            <h3>AI Scholarship Matching</h3>
            <p>Find scholarships based on your academic and personal profile.</p>
          </div>

          <div className="feature-card">
            <div>🏛️</div>
            <h3>Government Schemes</h3>
            <p>Discover welfare schemes and financial assistance programs.</p>
          </div>

          <div className="feature-card">
            <div>💬</div>
            <h3>AI Assistant</h3>
            <p>Get explanations and guidance about scholarship eligibility.</p>
          </div>

          <div className="feature-card">
            <div>📅</div>
            <h3>Deadline Tracker</h3>
            <p>Keep track of important scholarship application deadlines.</p>
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="how-it-works" id="how-it-works">
        <div className="section-heading">
          <span>SIMPLE PROCESS</span>
          <h2>How ScholarAI Works</h2>
        </div>

        <div className="steps">
          <div><strong>01</strong><h3>Create Profile</h3><p>Enter your student details.</p></div>
          <div><strong>02</strong><h3>Check Eligibility</h3><p>Let our system analyze your profile.</p></div>
          <div><strong>03</strong><h3>Get Matches</h3><p>Discover suitable opportunities.</p></div>
          <div><strong>04</strong><h3>Apply</h3><p>Follow application guidance.</p></div>
        </div>
      </section>

      {/* Footer */}
      <footer>
        <h2>ScholarAI</h2>
        <p>Making educational opportunities easier to discover.</p>
        <p className="backend-status">
          Backend: {backendStatus}
        </p>
        <p>© 2026 ScholarAI. All rights reserved.</p>
      </footer>

    </div>
  );
}

export default App;
