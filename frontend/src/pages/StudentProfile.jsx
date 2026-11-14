
import React, { useState } from "react";
import "./StudentProfile.css";

function StudentProfile({ user, onBack }) {
  const [formData, setFormData] = useState({
    fullName: user?.full_name || "",
    email: user?.email || "",
    state: "",
    district: "",
    category: "",
    course: "",
    branch: "",
    currentYear: "",
    marks: "",
    annualIncome: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const token = localStorage.getItem("access_token");

            const response = await fetch(
        `http://127.0.0.1:8000/student-profile/${user.id}`,
      {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                full_name: formData.fullName,
                email: formData.email,
                state: formData.state,
                district: formData.district,
                category: formData.category,
                course: formData.course,
                branch: formData.branch,
                current_year: formData.currentYear,
                previous_marks: Number(formData.marks),
                annual_family_income: Number(formData.annualIncome),
            }),
        }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Unable to save profile");
    }

    alert("Student profile saved successfully!");
  } catch (error) {
    alert(error.message);
    console.error("Profile save error:", error);
  }
};


  return (
    <div className="profile-container">
      <button
        type="button"
        onClick={onBack}
        style={{
            display: "block",
            padding: "12px 20px",
            backgroundColor: "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            marginBottom: "20px"
        }}
    >
        ← Back to Dashboard
    </button>

      <div className="profile-header">
        <h1>Student Profile</h1>
        <p>Complete your details to discover suitable scholarships.</p>
      </div>

      <form className="profile-form" onSubmit={handleSubmit}>
        <h2>Personal Information</h2>

        <input
          name="fullName"
          placeholder="Full Name"
          value={formData.fullName}
          onChange={handleChange}
          required
        />

        <input
          name="email"
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />

        <input
          name="state"
          placeholder="State"
          value={formData.state}
          onChange={handleChange}
          required
        />

        <input
          name="district"
          placeholder="District"
          value={formData.district}
          onChange={handleChange}
          required
        />

        <select name="category" value={formData.category} onChange={handleChange} required>
          <option value="">Select Category</option>
          <option value="General">General</option>
          <option value="OBC">OBC</option>
          <option value="SC">SC</option>
          <option value="ST">ST</option>
          <option value="EWS">EWS</option>
        </select>

        <h2>Educational Information</h2>

        <input
          name="course"
          placeholder="Course (e.g. B.Tech)"
          value={formData.course}
          onChange={handleChange}
          required
        />

        <input
          name="branch"
          placeholder="Branch (e.g. Computer Science)"
          value={formData.branch}
          onChange={handleChange}
          required
        />

        <select name="currentYear" value={formData.currentYear} onChange={handleChange} required>
          <option value="">Select Current Year</option>
          <option value="1">1st Year</option>
          <option value="2">2nd Year</option>
          <option value="3">3rd Year</option>
          <option value="4">4th Year</option>
        </select>

        <input
          name="marks"
          type="number"
          placeholder="Previous Academic Marks (%)"
          min="0"
          max="100"
          value={formData.marks}
          onChange={handleChange}
          required
        />

        <h2>Financial Information</h2>

        <input
          name="annualIncome"
          type="number"
          placeholder="Annual Family Income (₹)"
          min="0"
          value={formData.annualIncome}
          onChange={handleChange}
          required
        />

        <button type="submit" className="profile-submit">
          Save Profile
        </button>
      </form>
    </div>
  );
}

export default StudentProfile;
