
import React, { useState, useEffect } from "react";
import "./GovernmentSchemes.css";
import SchemeDetails from "./SchemeDetails";

function GovernmentSchemes({ onBack }) {
  const [selectedScheme, setSelectedScheme] = useState(null);
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchSchemes = async () => {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          "http://127.0.0.1:8000/government-schemes"
        );

        if (!response.ok) {
          throw new Error("Unable to fetch government schemes.");
        }

        const data = await response.json();

        setSchemes(data.schemes || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchSchemes();
  }, []);

  if (selectedScheme) {
    return (
      <SchemeDetails
        scheme={selectedScheme}
        onBack={() => setSelectedScheme(null)}
      />
    );
  }

  return (
    <div className="schemes-container">
      <button className="back-btn" onClick={onBack}>
        ← Back to Dashboard
      </button>

      <div className="schemes-header">
        <h1>Government Schemes</h1>
        <p>
          Explore financial assistance opportunities for students.
        </p>
      </div>

      {loading && (
        <p>Loading government schemes...</p>
      )}

      {error && (
        <div>
          <p>{error}</p>
          <button onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      )}

      {!loading && !error && (
        <>
          <p>Total Schemes Available: {schemes.length}</p>

          {schemes.length === 0 ? (
            <p>No government schemes available currently.</p>
          ) : (
            <div className="schemes-grid">
              {schemes.map((scheme) => (
                <div className="scheme-card" key={scheme.id}>
                  <span>
                    {scheme.category || scheme.scheme_type}
                  </span>

                  <h2>{scheme.scheme_name}</h2>

                  <p>{scheme.description}</p>

                  <button
                    className="view-details-btn"
                    onClick={() =>
                      setSelectedScheme({
                        ...scheme,
                        name: scheme.scheme_name,
                      })
                    }
                  >
                    View Details →
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default GovernmentSchemes;
