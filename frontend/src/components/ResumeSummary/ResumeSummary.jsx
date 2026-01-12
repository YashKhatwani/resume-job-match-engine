import React from 'react';
import './ResumeSummary.css';

export const ResumeSummary = ({ skills = ['Java', 'Spring Boot'], totalYoe = 2.5 }) => {
  return (
    <div className="summary-card">
      <h3>Resume Summary</h3>
      <div className="meta">
        <div className="yoe">Experience: <strong>{totalYoe} yrs</strong></div>
      </div>

      <div className="skills">
        {skills.map((s) => (
          <span key={s} className="skill-badge">{s}</span>
        ))}
        <button className="add-skill" aria-label="add-skill">+</button>
      </div>
    </div>
  );
};