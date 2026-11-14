
import React from "react";
import "./SchemeDetails.css";

function SchemeDetails({ scheme, onBack }) {
  if (!scheme) {
    return <p>Scheme details not available.</p>;
  }

  // Display unavailable fields clearly
  const showValue = (value) => {
    if (value === null || value === undefined || value === "") {
      return "Not specified";
    }

    return value;
  };

  // Format financial values
  const formatAmount = (value) => {
    if (value === null || value === undefined || value === "") {
      return "Not specified";
    }

    return `₹${Number(value).toLocaleString("en-IN")}`;
  };

  // Reusable information row
  const DetailRow = ({ label, value }) => (
    <div className="detail-row">
      <strong>{label}</strong>
      <span>{showValue(value)}</span>
    </div>
  );

  const schemeName = scheme.scheme_name || scheme.name;

  return (
    <div className="scheme-details-container">

      <button className="back-btn" onClick={onBack}>
        ← Back to Government Schemes
      </button>

      <div className="scheme-details-card">

        {/* Scheme Header */}
        <span className="scheme-category">
          {showValue(scheme.category)}
        </span>

        <h1>{schemeName}</h1>

        <p>{showValue(scheme.description)}</p>

        <hr />

        {/* Basic Information */}
        <section className="details-section">
          <h2>About this Scheme</h2>

          <DetailRow
            label="Government Level"
            value={scheme.government_level}
          />

          <DetailRow
            label="Applicable State / UT"
            value={scheme.state_ut}
          />

          <DetailRow
            label="Scheme Type"
            value={scheme.scheme_type}
          />

          <DetailRow
            label="Benefit Type"
            value={scheme.benefit_type}
          />

          <DetailRow
            label="Education Level"
            value={scheme.education_level}
          />
        </section>

        <hr />

        {/* Eligibility */}
        <section className="details-section">
          <h2>Eligibility Criteria</h2>

          <p>{showValue(scheme.eligibility_criteria)}</p>

          <DetailRow
            label="Annual Family Income Limit"
            value={
              scheme.annual_income_limit == null
                ? null
                : formatAmount(scheme.annual_income_limit)
            }
          />

          <DetailRow
            label="Minimum Marks"
            value={
              scheme.minimum_marks == null
                ? null
                : `${scheme.minimum_marks}%`
            }
          />

          <DetailRow
            label="Eligible Courses"
            value={scheme.eligible_courses}
          />

          <DetailRow
            label="Eligible Institutions"
            value={scheme.eligible_institutions}
          />
        </section>

        <hr />

        {/* Financial Benefits */}
        <section className="details-section">
          <h2>Financial Benefits</h2>

          <p>{showValue(scheme.benefits)}</p>

          <DetailRow
            label="Scholarship Amount"
            value={
              scheme.scholarship_amount == null
                ? null
                : formatAmount(scheme.scholarship_amount)
            }
          />

          <DetailRow
            label="Maximum Education Loan"
            value={
              scheme.maximum_loan_amount == null
                ? null
                : formatAmount(scheme.maximum_loan_amount)
            }
          />

          <DetailRow
            label="Interest Rate"
            value={
              scheme.interest_rate == null
                ? null
                : `${scheme.interest_rate}%`
            }
          />

          <DetailRow
            label="Interest Subvention"
            value={
              scheme.interest_subvention_rate == null
                ? null
                : `${scheme.interest_subvention_rate}%`
            }
          />

          <DetailRow
            label="Repayment Period"
            value={
              scheme.repayment_period_years == null
                ? null
                : `${scheme.repayment_period_years} years`
            }
          />

          <DetailRow
            label="Moratorium Period"
            value={scheme.moratorium_period}
          />

          <DetailRow
            label="Collateral Requirement"
            value={scheme.collateral_requirement}
          />

          <DetailRow
            label="Credit Guarantee Details"
            value={scheme.credit_guarantee_details}
          />
        </section>

        <hr />

        {/* Documents */}
        <section className="details-section">
          <h2>Required Documents</h2>
          <p>{showValue(scheme.required_documents)}</p>
        </section>

        <hr />

        {/* Renewal */}
        <section className="details-section">
          <h2>Renewal Conditions</h2>
          <p>{showValue(scheme.renewal_conditions)}</p>
        </section>

        <hr />

        {/* Application Information */}
        <section className="details-section">
          <h2>Application Information</h2>

          <DetailRow
            label="Application Start Date"
            value={scheme.application_start_date}
          />

          <DetailRow
            label="Application Deadline"
            value={scheme.application_deadline}
          />

          <div className="scheme-links">
            <h3>Official Links</h3>

            {scheme.application_url && (
              <p>
                <a
                  href={scheme.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Apply for this Scheme →
                </a>
              </p>
            )}

            {scheme.official_source_url && (
              <p>
                <a
                  href={scheme.official_source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View Official Guidelines →
                </a>
              </p>
            )}

            {!scheme.application_url &&
              !scheme.official_source_url && (
                <p>Official links are not available.</p>
              )}
          </div>
        </section>

      </div>
    </div>
  );
}

export default SchemeDetails;
